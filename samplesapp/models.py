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
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    sample_type = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    remained = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    access_key = models.CharField(max_length=32, unique=True, blank=True)


    def save(self, *args, **kwargs):
        # Jeśli obiekt nie został jeszcze zapisany w bazie (nowy obiekt)
        if not self.pk:
            if self.remained is None:
                self.remained = self.quantity
            if not self.access_key:
                self.access_key = get_random_string(length=32)
        else:
        # Jeśli edytujemy istniejący obiekt, zapewnij, by access_key nie był aktualizowany do pustej wartości.
            self.access_key = SamplesModel.objects.get(pk=self.pk).access_key


        super(SamplesModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.sample_name

class SampleUsageModel(models.Model):
    sample = models.ForeignKey(SamplesModel, on_delete=models.CASCADE, related_name='usages')
    date_used = models.DateField(auto_now_add=True)
    quantity_used = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Aktualizuj wartość `remained` w `SamplesModel`
        self.sample.remained -= self.quantity_used
        self.sample.save()

    def __str__(self):
        return f"{self.sample.sample_name} - {self.date_used} - {self.quantity_used}"