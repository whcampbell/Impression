from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
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

def messages(request, username) :
    # User verification
    if (request.user.username != username) :
        raise PermissionDenied

    # Get user/message objects
    user = CustomUser.objects.get(username=username)
    messages = Message.objects.filter(receiver=user.pk)

    # get latest message per sender
    finalized_messages = []
    senders = []
    for message in messages :

        # if no messages found yet for this sender - just add
        if (message.sender not in senders) :
            senders.append(message.sender)
            finalized_messages.append([message.sender, message])
        # should be ordered by model metadata
        # first one will always be latest

    # send 'er
    return render(request, 'users/messages.html', {'messages':finalized_messages})

def message_detail(request, id) :
    message = Message.objects.get(pk=id)

    if (message.receiver.id != request.user.id) :
        raise PermissionDenied
    
    message.read = True
    message.save()
    context = {
        'message':message,
        'username':request.user.username,
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

            return HttpResponseRedirect(reverse('users:messages', args=[request.user.username]))

    else :
        form = MessageForm()
        form.fields['receiver'].choices = populate_recipient_choices(request.user)

    return render(request, 'users/message_compose.html', {'form':form})

def make_friends(request, sender) :
    friend_1 = CustomUser.objects.get(username=sender)
    friend_2 = CustomUser.objects.get(username=request.user)

    friend_1.friends.add(friend_2)

    return HttpResponseRedirect(reverse('users:messages', args=[request.user.username]))

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
