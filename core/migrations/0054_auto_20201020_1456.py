# Generated by Django 2.2 on 2020-10-20 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20201020_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=36000),
        ),
    ]
