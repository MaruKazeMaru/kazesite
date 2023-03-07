from django import forms
from django.contrib.auth.forms import AuthenticationForm
from . import models

class LoginForm(AuthenticationForm):
	class Meta:
		model = models.MyUser
		fields = ['email', 'password']

class CreateUserForm(forms.Form):
	username = forms.CharField(max_length=32, initial="guest")
	email = forms.EmailField()
