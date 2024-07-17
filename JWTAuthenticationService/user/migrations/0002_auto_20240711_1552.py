# Generated by Django 3.1.3 on 2024-07-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='published_from_date',
        ),
        migrations.AddField(
            model_name='user',
            name='number_of_news_articles',
            field=models.IntegerField(default=3),
        ),
    ]