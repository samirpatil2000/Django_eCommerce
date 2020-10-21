# Generated by Django 2.2 on 2020-10-20 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_auto_20201020_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=39000),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]