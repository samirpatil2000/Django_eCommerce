# Generated by Django 2.2 on 2020-10-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20201020_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=32000),
        ),
    ]