# Generated by Django 5.1 on 2024-08-26 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0006_alter_stream_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
