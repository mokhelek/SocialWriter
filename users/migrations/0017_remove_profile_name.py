# Generated by Django 4.0.4 on 2022-06-22 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_profile_avatar_profile_bio_profile_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
    ]