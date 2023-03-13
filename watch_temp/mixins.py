from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.mixins import UserPassesTestMixin

class CanAccessAppMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.can_access_watch_temp

	def handle_no_permission(self):
		raise Http404("")

class SuperLoginRequiredMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_superuser

	def handle_no_permission(self):
		return redirect('/login_super/?next=' + self.request.path)

