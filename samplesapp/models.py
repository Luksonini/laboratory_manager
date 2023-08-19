from django.db import models
from django.core.validators import MinValueValidator
from django.utils.crypto import get_random_string

# Create your models here.
class SamplesModel(models.Model):
    sample_date = models.DateField(auto_now_add=True)
    sample_name = models.CharField(max_length=200)
    species = models.CharField(max_length=50, blank=True, null=True)
    owner = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200)
    quantity = models.FloatField(default=0, validators=[MinValueValidator(0)])
    sample_type = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    remained = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    access_key = models.CharField(max_length=32, unique=True, blank=True)


    def save(self, *args, **kwargs):
        if self.remained is None:
            self.remained = self.quantity
        else: 
            self.remained = round(self.remained, 2)
        if not self.access_key:
            self.access_key = get_random_string(length=32)
        super(SamplesModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.sample_name