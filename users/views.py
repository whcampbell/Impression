from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from .forms import UserRegistrationForm, LoginForm, MessageForm
from .models import CustomUser, Message

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
    user = CustomUser.objects.get(username=username)
    are_friends = request.user.friends.all().contains(user)
    context = {
        'this_pages_user':user,
        'are_friends':are_friends,
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
    try :
        Message.objects.get(
            sender=friend_1, 
            receiver=friend_2, 
            is_friend_request=True).delete()
    except ObjectDoesNotExist :
        raise PermissionDenied

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

# Create your views here.
