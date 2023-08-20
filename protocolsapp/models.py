from django.db import models

# Create your models here.
class Protocols(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    file = models.FileField(upload_to='uploads')

    def __str__(self):
        return self.name