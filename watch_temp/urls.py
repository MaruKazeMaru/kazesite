from django.urls import path 
from . import views

app_name='watch_temp'
urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('about_original_system/', views.AboutOriginalSystem.as_view(), name='about_original_system'),
	path('create_building/',    views.CreateBuilding.as_view(),    name='create_building'),
	path('create_thermometer/', views.CreateThermometer.as_view(), name='create_thermometer'),
	path('create_floor/<int:building_id>/<int:floor>', views.CreateFloor.as_view(), name="create_floor"),
	path('set_thermometer_pos/<int:floor_id>', views.SetThermometerPos.as_view(), name="set_thermometer_pos"),
	path('detail_building/<int:pk>',    views.DetailBuilding.as_view(),    name='detail_building'),
	path('detail_thermometer/<int:pk>', views.DetailThermometer.as_view(), name="detail_thermometer"),
	path('detail_floor/<int:pk>',       views.DetailFloor.as_view(),       name="detail_floor"),
]
