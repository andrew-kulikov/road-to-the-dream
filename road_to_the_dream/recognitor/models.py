from django.db import models


class Post(models.Model):
    image = models.ImageField(upload_to='images/')
