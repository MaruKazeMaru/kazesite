from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from . import models, forms

class Index(TemplateView):
	template_name = "my_user/index.html"

class Login(LoginView):
	form_class = forms.LoginForm
	template_name = "my_user/login.html"
