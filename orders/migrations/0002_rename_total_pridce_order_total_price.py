# Generated by Django 5.1.3 on 2024-11-14 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_pridce',
            new_name='total_price',
        ),
    ]
