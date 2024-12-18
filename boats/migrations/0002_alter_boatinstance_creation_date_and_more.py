# Generated by Django 5.1.3 on 2024-11-23 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boatinstance',
            name='creation_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='boatmodel',
            name='image',
            field=models.ImageField(upload_to='boat_images/'),
        ),
    ]
