from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = "wili/index.html"


class ToolsIndexView(TemplateView):
    template_name = "wili/tools/index.html"


class ToolsRefView(TemplateView):
    template_name = "wili/tools/ref.html"
