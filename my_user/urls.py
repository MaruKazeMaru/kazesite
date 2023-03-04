from django.urls import path 
from . import views

app_name='my_user'
urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('login/', views.Login.as_view(), name='login'),
]
