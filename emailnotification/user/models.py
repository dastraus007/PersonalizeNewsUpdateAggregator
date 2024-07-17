from django.db import models

class user(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=120)
    politics_preference = models.IntegerField(default=0)
    business_preference = models.IntegerField(default=0)
    technology_preference = models.IntegerField(default=0)
    sports_preference = models.IntegerField(default=0)
    entertainment_preference = models.IntegerField(default=0)
