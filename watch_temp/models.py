from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Building(models.Model):
	name = models.CharField(max_length=64)
	floor_count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
	comment = models.TextField(max_length=1000)

class FloorImage(models.Model):
	image = models.ImageField(upload_to="images/floor/")

class Floor(models.Model):
	building = models.ForeignKey(Building, on_delete=models.CASCADE)
	name = models.CharField(max_length=64)
	image = models.ImageField(upload_to="images/floor/")
	floor = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
	comment = models.TextField(max_length=1000)
