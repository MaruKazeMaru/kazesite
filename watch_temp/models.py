from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Building(models.Model):
	name = models.CharField(max_length=64)
	floor_count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
	comment = models.TextField(max_length=1000, blank=True, null=True)


class Floor(models.Model):
	building = models.ForeignKey(Building, on_delete=models.CASCADE)
	name = models.CharField(max_length=64)
	image = models.ImageField(upload_to="images/floor/")
	floor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
	comment = models.TextField(max_length=1000, blank=True, null=True)


class Thermometer(models.Model):
	floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, blank=True, null=True)
	name = models.CharField(max_length=64, blank=True, null=True)
	serial = models.CharField(max_length=64, unique=True)
	pos_x = models.FloatField(blank=True, null=True)
	pos_y = models.FloatField(blank=True, null=True)
	comment = models.TextField(max_length=1000, blank=True, null=True)
