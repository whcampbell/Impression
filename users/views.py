from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from .forms import UserRegistrationForm, LoginForm, MessageForm, CustomChangeForm, BlogForm
from .models import CustomUser, Message, BlogPost
from random import sample

# Helpers
def populate_recipient_choices(user) :
    friends = user.friends.all()
    choice_list = []
    for friend in friends :
        choice_name = friend.username
        choice_list.append((choice_name, choice_name))

    return choice_list

# Views
class SignupView(CreateView) :
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:login")
    template_name = 'users/signup.html'

class WritePostView(CreateView) :
    form_class = BlogForm
    template_name = 'users/write_post.html'

    def get_success_url(self) :
        return reverse('users:profile', args=[self.request.user.username])
    
    def form_valid(self, form) :
        BlogPost.objects.create(
            user=self.request.user,
            title=form.cleaned_data['title'],
            body=form.cleaned_data['body'],
            image=form.cleaned_data['image'],
            alt_text=form.cleaned_data['alt_text']
        )
        return HttpResponseRedirect(self.get_success_url())

class UserUpdateView(UserPassesTestMixin, UpdateView) :
    model = CustomUser
    form_class = CustomChangeForm
    template_name = 'users/user_update.html'
    raise_exception = True

    def get_success_url(self) :
        return reverse('users:profile', args=[self.get_object().username])
    
    def test_func(self) :
        return self.request.user.pk == self.get_object().pk

class PasswordView(PasswordChangeView) :
    template_name = 'users/change_password.html'

    def get_success_url(self) :
        return reverse("users:profile", args=[self.request.user.username])

def login_view(request) :
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None :
                login(request, user)
                return HttpResponseRedirect(reverse("welcome"))
            # redirect to a new URL:
            else :
                form.add_error("username", "User Not Found")
                return render(request, 'users/login.html', {'form':form})
            
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form':form})

def logout_view(request) :
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))

def profile(request, username) :
    host = CustomUser.objects.get(username=username)
    guest = request.user
    are_friends = False
    if guest.is_authenticated :
        are_friends = guest.friends.all().contains(host)

    friend_messages = list(host.received_messages.filter(sender=guest))
    request_pending = len(friend_messages) > 0 and friend_messages[0].is_friend_request

    last_post = host.blogpost_set.first()
    context = {
        'host_user':host,
        'is_logged_in':guest.is_authenticated,
        'are_friends':are_friends,
        'request_pending':request_pending,
        'last_post':last_post,
    }
    return render(request, 'users/profile.html', context)

def messages(request) :
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse('users:login'))

    # I hear that this only works on Postgres!
    # (select distinct on a single field rather than the whole object)
    messages = Message.objects.order_by('sender', '-time_sent').distinct(
        'sender').filter(receiver=request.user)
    
    # send 'er
    return render(request, 'users/messages.html', {'messages':messages})

def message_detail(request, id) :
    message = Message.objects.get(pk=id)

    if (message.receiver.id != request.user.id) :
        raise PermissionDenied
    
    message.read = True
    message.save()

    other_messages = Message.objects.filter(
        sender=message.sender,
        receiver=message.receiver).exclude(pk=id)
    
    context = {
        'curr_message':message,
        'username':request.user.username,
        'messages':other_messages,
    }
    return render(request, 'users/message_detail.html', context)

def message_create(request) :
    if request.method == "POST" :
        form = MessageForm(request.POST)
        form.fields['receiver'].choices = populate_recipient_choices(request.user)
        if not form.is_valid() :
            return render(request, 'users/message_compose.html', {'form':form})
        else :
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            receiver = form.cleaned_data['receiver']

            for name in receiver :
                to_user = CustomUser.objects.get(username=name)
                from_user = request.user
                new_message = Message(
                    title=title, 
                    body=body, 
                    sender = from_user,
                    receiver = to_user,
                    read=False
                    )
                new_message.save()

            return HttpResponseRedirect(reverse('users:messages'))

    else :
        form = MessageForm()
        form.fields['receiver'].choices = populate_recipient_choices(request.user)

    return render(request, 'users/message_compose.html', {'form':form})

def make_friends(request, sender) :
    # consistent between code and tests - one is sender, two is receiver
    friend_1 = CustomUser.objects.get(username=sender)
    friend_2 = request.user

    # Delete the friend request message
    # if it doesn't exist, someone may be trying to cheat the friend system
    req_list = Message.objects.filter(
        sender=friend_1, 
        receiver=friend_2, 
        is_friend_request=True)
    if (req_list.count() == 0) :
        raise PermissionDenied
    req_list.delete()

    friend_1.friends.add(friend_2)

    return HttpResponseRedirect(reverse('users:messages'))

def send_friends(request, receiver) :
    new_friend = CustomUser.objects.get(username=receiver)

    Message.objects.create(
        title = "Friend Request From " + request.user.username,
        body = "",
        sender = request.user,
        receiver = new_friend,
        is_friend_request = True
    ).save()

    return HttpResponseRedirect(reverse('users:profile', args=[receiver]))

def manage_friends(request) :
    friends = request.user.friends.all()
    return render(request, 'users/manage_friends.html', {'friends':friends})

def remove_friend(request, username) :
    ex_friend = CustomUser.objects.get(username=username)
    request.user.friends.remove(ex_friend)
    return HttpResponseRedirect(reverse('users:manage_friends'))

def gallery(request) :

    # yes evaluating the whole set is gross
    # but that's the simplest way to randomize
    # as long as there's only five users that won't matter
    users = list(CustomUser.objects.all())
    users = sample(users, 5)

    return render(request, 'users/gallery.html', {'users':users})

def read_post(request, id) :
    post = get_object_or_404(BlogPost, pk=id)
    post_list = BlogPost.objects.filter(user=post.user).exclude(pk=post.pk)
    context = {
        'curr_post':post,
        'post_list':post_list,
    }
    return render(request, 'users/read_post.html', context)

def delete_post(request, id) :
    post = get_object_or_404(BlogPost, pk=id)

    if (post.user != request.user) :
        raise PermissionDenied

    post.delete()
    return HttpResponseRedirect(reverse('users:profile', args=[request.user.username]))
