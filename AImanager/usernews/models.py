from django.db import models

class usernews(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)

