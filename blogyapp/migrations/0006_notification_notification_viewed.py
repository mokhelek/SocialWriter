# Generated by Django 4.0.4 on 2023-01-12 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogyapp', '0005_notification_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_viewed',
            field=models.BooleanField(default=False),
        ),
    ]
