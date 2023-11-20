from django.db import models

# Create your models here.
class Protocols(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, default='blbl')
    description = models.CharField(max_length=500, blank=True, null=True)
    method = models.TextField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='uploads', blank=True, null=True)

    def __str__(self):
        return self.title

