# Generated by Django 5.1.3 on 2024-11-23 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boats', '0003_remove_boatinstance_price_per_day_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='boatmodel',
            name='release_date',
            field=models.DateField(),
            preserve_default=False,
        ),
    ]
