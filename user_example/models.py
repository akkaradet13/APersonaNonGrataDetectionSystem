from django.db import models

# Create your models here.
class Post(models.Model):
    Name = models.CharField(max_length=30)
    Time = models.CharField(max_length=30)
    Image = models.ImageField(upload_to='image', blank=True)

    def __str__(self):
        return self.Name