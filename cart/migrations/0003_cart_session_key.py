# Generated by Django 5.1.3 on 2024-11-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_cart_end_date_remove_cart_start_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
