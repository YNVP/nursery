from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Nursery 
from django.forms import ValidationError


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        # Get the email
        email = self.cleaned_data['email']

        # Check to see if any users already exist with this email as a username.
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

class NurseryRegisterForm(forms.ModelForm):
    class Meta:
        model = Nursery
        fields = ['name','image']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class NurseryUpdateForm(forms.ModelForm):
    class Meta:
        model = Nursery
        fields = ['name', 'image']
