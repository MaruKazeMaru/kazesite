from django.contrib.auth.forms import AuthenticationForm
from . import models

class LoginForm(AuthenticationForm):
	class Meta:
		model = models.MyUser
		fields = ['email', 'password']
