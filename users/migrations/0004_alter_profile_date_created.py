# Generated by Django 4.0.4 on 2023-01-13 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]