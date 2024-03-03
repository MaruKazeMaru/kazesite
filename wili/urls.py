from django.urls import path

from . import views

app_name = "wili"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("tools", views.ToolsIndexView.as_view(), name="tools_index"),
    path("tools/reference", views.ToolsRefView.as_view(), name="tools_ref"),
]
