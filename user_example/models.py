from django.db import models

# Create your models here.
class Post(models.Model):
    postName = models.CharField(max_length=30)
    description = models.TextField()
    time = models.CharField(max_length=30)
    image = models.ImageField(upload_to='image', blank=True)

    def __str__(self):
        return self.postName