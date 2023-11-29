# yourapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AuthUser


class SignUpForm(UserCreationForm):
    fullname = forms.CharField(required=True, max_length=69)
    birthdate = forms.DateField(required=True)

    class Meta:
        model = AuthUser
        fields = ['username', 'email', 'password1', 'password2']
