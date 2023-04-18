from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import PasswordInput, DateInput, Form, CharField
from .models import CustomUser

class UserRegistrationForm(UserCreationForm) :
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'artist_since',]
        widgets = {
            'password' : PasswordInput(),
            'artist_since' : DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
        }

class CustomChangeForm(UserChangeForm) :
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'artist_since',]

class LoginForm(Form) :
    username = CharField(label="Username", required=True, max_length=20)
    password = CharField(label="Password", required=True, widget=PasswordInput)