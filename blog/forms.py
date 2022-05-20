from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Profile


class SignUpForm(UserCreationForm):
    error_css_class = 'formError'

    email = forms.EmailField(label='email', max_length=255, widget=forms.EmailInput(
        attrs={
            'placeholder': 'Email',
            'class': 'textEdit'
        }
    ))
    name = forms.CharField(label='name', max_length=20, widget=forms.TextInput(
        attrs={
            'placeholder': 'Name',
            'class': 'textEdit'
        }
    ))
    surname = forms.CharField(label='surname', max_length=20, widget=forms.TextInput(
        attrs={
            'placeholder': 'Surname',
            'class': 'textEdit'
        }
    ))
    address = forms.CharField(label='address', max_length=200, widget=forms.TextInput(
        attrs={
            'placeholder': 'Address',
            'class': 'textEdit'
        }
    ))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'textEdit'
        }
    ))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm password',
            'class': 'textEdit'
        }
    ))

    class Meta:
        model = Profile
        fields = ['email', 'name', 'surname', 'address', 'password1', 'password2']

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = Profile.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = Profile.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['name'],
            self.cleaned_data['surname'],
            self.cleaned_data['address'],
            self.cleaned_data['password1']
        )
        return user


class LoginForm(AuthenticationForm):
    error_css_class = 'formError'

    email = forms.EmailField(label='email', max_length=255, widget=forms.EmailInput(
        attrs={
            'placeholder': 'Email',
            'class': 'textEdit'
        }
    ))

    password1 = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'textEdit'
        }
    ))
