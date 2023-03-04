from django.urls import path 
from . import views

app_name='chain_move'
urlpatterns = [
	path('controll', views.controll, name='controll'),
]
