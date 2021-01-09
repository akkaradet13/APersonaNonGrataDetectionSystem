from django.db import models
from datetime import datetime

# Create your models here.
class Post(models.Model):
    Name = models.CharField(max_length=50, default='0')
    DateTime = models.DateTimeField(default='0')
    Image = models.ImageField(upload_to='image', blank=True, null=True)

    def __str__(self):
        return self.Name


        # https://www.geeksforgeeks.org/datetimefield-django-models/