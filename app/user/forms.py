from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class MyUserRegisterForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('phone_number', 'email', 'first_name')
