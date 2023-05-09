from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

def create_choices() :
    users = CustomUser.objects.all()
    names = []
    for user in users :
        names.append((user.username, user.username))
    return names

USER_CHOICES = create_choices()

class UserRegistrationForm(UserCreationForm) :
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'artist_since', 'main_photo',]
        widgets = {
            'password' : forms.PasswordInput(),
            'artist_since' : forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
        }

class CustomChangeForm(UserChangeForm) :
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'artist_since', 'main_photo',]

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