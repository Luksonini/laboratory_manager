from django.db import models

class Reagents(models.Model):
    reagent_name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200, blank=True, null=True)
    firm = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200)
    cat_number = models.CharField(max_length=200, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    purchase_date =  models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.reagent_name
