from django.db import models


# Create your models here.
class Entry(models.Model):
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    hashword = models.CharField(max_length=255)
    website = models.CharField(max_length=100)

    def __str__(self):
        return self.name
