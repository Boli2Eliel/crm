from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

INPUT_CLASS = " w-full py-2 px-6 rounded-xl"

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Votre nom d'utilisateur",
        #'class':"w-full form-group py-4 px-6 rounded-xl bg-gray-100"
        'class':INPUT_CLASS
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Votre mot de passe",
        #'class': "w-full form-group py-4 px-6 rounded-xl bg-gray-100"
        'class': INPUT_CLASS
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Votre nom d'utilisateur",
        'class': INPUT_CLASS
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': "Votre adresse mail",
        'class': INPUT_CLASS
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Votre mot de passe",
        'class': INPUT_CLASS
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Repetez votre mot de passe",
        'class': INPUT_CLASS
    }))