from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, BlogPost

# Form to sign up a new user
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

# Form to edit a user's profile information
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

# Form to log in
class LoginForm(forms.Form) :
    username = forms.CharField(label="Username", required=True, max_length=20)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)

# Form to create a new message
class MessageForm(forms.Form) :
    title = forms.CharField(label="Title", required=True, max_length=64)
    body = forms.CharField(label='', required=True, widget=forms.Textarea)
    receiver = forms.MultipleChoiceField(
        label='Send to:',
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )

# Form to create a new blog post
class BlogForm(forms.ModelForm) :

    class Meta :
        model = BlogPost
        fields = ['title', 'body', 'image', 'alt_text',]