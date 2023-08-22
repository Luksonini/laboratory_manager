from django.db import models

# Create your models here.
class Protocols(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    method = models.TextField(max_length=1000)    
    file = models.FileField(upload_to='uploads')

    def __str__(self):
        return self.title