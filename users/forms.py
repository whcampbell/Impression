from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class UserRegistrationForm(UserCreationForm) :
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'artist_since', 'main_photo', 'description',]
        widgets = {
            'password' : forms.PasswordInput(),
            'artist_since' : forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
        }

class CustomChangeForm(UserChangeForm) :
    # no ugly password message
    password = None
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'artist_since', 'main_photo', 'description',]
        widgets = {
            'artist_since' : forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
        }

class LoginForm(forms.Form) :
    username = forms.CharField(label="Username", required=True, max_length=20)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)

class MessageForm(forms.Form) :
    title = forms.CharField(label="Title", required=True, max_length=64)
    body = forms.CharField(label='', required=True, widget=forms.Textarea)
    receiver = forms.MultipleChoiceField(
        label='Send to:',
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )