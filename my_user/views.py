import string
import secrets
import datetime
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from . import forms, models, mixins

def generate_password(length=10):
	letter_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
	p = ''
	for i in range(length):
		p += secrets.choice(letter_set)
	return p

class Index(TemplateView):
	template_name = "my_user/index.html"

class Login(LoginView):
	form_class = forms.LoginForm
	template_name = "my_user/login.html"

class CreateUser(mixins.SuperLoginRequiredMixin, FormView):
	template_name = "my_user/create_user.html"
	form_class = forms.CreateUserForm
	success_url = reverse_lazy("my_user:index")
	"""
	def post(self, request):
		if 'email' in request.POST:
			try:
				user = models.MyUser.objects.get(email=request.POST['email'])
			except: pass
			else:
				err_msgs = ['入力したメールアドレスは既に登録されています']
				return render(request, "my_user/error.html", {'error_messages': err_msgs})
		return super().post(request)
	"""
	def form_valid(self, form):
		email = form.cleaned_data.get('email')
		user = None
		try:
			user = models.MyUser.objects.get(email=email)
		except:
			user = models.MyUser.objects.create_user(
				username = form.cleaned_data.get('username'),
				email = email,
				password = generate_password(length=10)
			)
		key = secrets.choice(string.ascii_lowercase) + generate_password(length=63)
		models.ActivateToken.objects.create(
			user = user,
			key = key,
			expire_time = datetime.datetime.now() + datetime.timedelta(days=1)
		)
		body = "下記リンクよりログインできます。<br>"
		if settings.DEBUG:
			domain = "localhost:8000"
		else:
			domain = ""
		body += "http://" + domain + reverse('my_user:login_by_activate_token', kwargs={'key': key}) + "<br>"
		body += "リンクの有効期間は24時間です。<br>"
		body += "<br>当メールにお心当たりがない場合は、お手数ですが削除をお願いいたします。"
		from .mailmemo import from_email
		mail = EmailMessage(
			subject='kazesiteへのログインについて',
			body = body,
			from_email = from_email,
			to = [email]
		)
		mail.send()
		return super().form_valid(form)


def login_by_activate_token(req, key):
	token = get_object_or_404(models.ActivateToken, key=key)
	login(req, token.user)
	return redirect(reverse('my_user:index'))
