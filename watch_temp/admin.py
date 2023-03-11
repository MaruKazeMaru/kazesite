from django.contrib import admin
from . import models

admin.site.register(models.Building)
admin.site.register(models.Floor)
admin.site.register(models.Thermometer)
