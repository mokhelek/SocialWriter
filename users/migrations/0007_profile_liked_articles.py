# Generated by Django 4.0.4 on 2023-01-13 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogyapp', '0007_like'),
        ('users', '0006_remove_profile_liked_articles'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='liked_articles',
            field=models.ManyToManyField(blank=True, related_name='liked_articles', to='blogyapp.entry'),
        ),
    ]
