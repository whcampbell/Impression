from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm) :
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password' : forms.PasswordInput(),
        }

class LoginForm(forms.Form) :
    username = forms.CharField(label="Username", required=True, max_length=20)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)