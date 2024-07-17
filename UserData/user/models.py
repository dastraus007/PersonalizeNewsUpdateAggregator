from datetime import datetime, date

from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=120)#not neet it atomatic
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)  # Use EmailField for validation
    preference = models.TextField(blank=True, null=True)  # Use TextField for larger data
    is_staff = models.BooleanField(default=False)
    news_categories = models.JSONField(default=dict)  # Ensure it's a callable
    preferred_channel = models.CharField(max_length=255, default="email")
    number_of_news_articles = models.IntegerField(default=3)
    language = models.CharField(max_length=255, default="en")
    username = None  # Not necessary but kept for clarity
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
