from django.urls import path 
from . import views

app_name='my_user'
urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('login/', views.Login.as_view(), name='login'),
	path('create_user/', views.CreateUser.as_view(), name='create_user'),
	path('login_by_activate_token/<slug:key>', views.login_by_activate_token, name='login_by_activate_token')
]
