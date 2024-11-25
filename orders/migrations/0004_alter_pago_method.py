# Generated by Django 5.1.3 on 2024-11-24 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_end_date_remove_order_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='method',
            field=models.CharField(choices=[('on_site', 'Pagar en sitio'), ('online', 'Pagar en línea')], max_length=50),
        ),
    ]
