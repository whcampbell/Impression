from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.views import generic
from django.urls import reverse, reverse_lazy
from .forms import UserRegistrationForm, LoginForm
from .models import CustomUser

class SignupView(generic.CreateView) :
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
    return render(request, 'users/profile.html', {'this_pages_user':user})
# Create your views here.
