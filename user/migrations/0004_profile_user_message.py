# Generated by Django 3.1.7 on 2022-06-12 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20220607_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_message',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
