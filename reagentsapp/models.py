from django.db import models
from django.core.validators import MinValueValidator

class Reagents(models.Model):
    UNIT_CHOICES = (
        ('-', '-'),
        ('ml', 'ml'),
        ('ul', 'ul'),
        ('g', 'g'),
        ('mg', 'mg'),
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

    def save(self, *args, **kwargs):
        if self.remained is None:  # Sprawdzamy, czy remained jest pusty
            self.remained = self.quantity
        else: 
            self.remained = round(self.remained, 2)
        super(Reagents, self).save(*args, **kwargs)

    def __str__(self):
        return self.reagent_name
    
  



