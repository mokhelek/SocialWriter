# Generated by Django 4.0.4 on 2022-06-15 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_profile_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='posts',
        ),
    ]