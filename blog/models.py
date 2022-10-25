from email.mime import image
from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Blog(models.Model):
    title =models.CharField(max_length=200)
    description = models.TextField()
    body = HTMLField()
    image = models.ImageField()
    slug  = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


        