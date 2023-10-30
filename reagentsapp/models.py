from django.db import models
from django.core.validators import MinValueValidator
from django.utils.crypto import get_random_string

class Reagents(models.Model):
    UNIT_CHOICES = (
        ('-', '-'),
        ('ml', 'ml'),
        ('μl', 'μl'),
        ('g', 'g'),
        ('mg', 'mg'),
        ('μg', 'μg'),
        ('ug', 'ug'),
        ('szt', 'sztuk'),
    )
    reagent_name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200, blank=True, null=True)
    firm = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200)
    cat_number = models.CharField(max_length=200, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    purchase_date =  models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.FloatField(default=0, validators=[MinValueValidator(0)])
    remained = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES, default='-')
    access_key = models.CharField(max_length=32, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if self.remained is None:  # Sprawdzamy, czy remained jest pusty
            self.remained = self.quantity
        else:
            self.remained = round(self.remained, 2)
        if not self.access_key:
            self.access_key = get_random_string(length=32)  # generowanie klucza
        super(Reagents, self).save(*args, **kwargs)


    def __str__(self):
        return self.reagent_name





