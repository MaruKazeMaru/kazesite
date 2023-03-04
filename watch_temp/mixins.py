from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

class MyLoginRequiredMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_active

	def handle_no_permission(self):
		return redirect('/login/?next=' + self.request.path)

class SuperLoginRequiredMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_superuser

	def handle_no_permission(self):
		return redirect('/login_super/?next=' + self.request.path)

