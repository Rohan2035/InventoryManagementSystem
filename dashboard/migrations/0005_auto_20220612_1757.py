# Generated by Django 3.1.7 on 2022-06-12 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20220612_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='out_of_stock',
            field=models.BooleanField(null=True),
        ),
    ]
