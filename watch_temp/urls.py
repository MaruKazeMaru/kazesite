from django.urls import path 
from . import views

app_name='watch_temp'
urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('about_original_system/', views.AboutOriginalSystem.as_view(), name='about_original_system'),
	path('create_building/', views.CreateBuilding.as_view(), name='create_building'),
	path('detail_building/<int:pk>', views.DetailBuilding.as_view(), name='detail_building'),
	path('create_floor/<int:building_id>/<int:floor>', views.CreateFloor.as_view(), name="create_floor"),
	path('detail_floor/<int:pk>', views.DetailFloor.as_view(), name="detail_floor"),
]
