# Generated by Django 5.1 on 2024-08-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0007_profile_department_profile_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='user-vector.jpg', null=True, upload_to=''),
        ),
    ]
