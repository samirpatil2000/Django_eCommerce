# Generated by Django 2.2 on 2020-10-19 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20201019_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=19000),
        ),
    ]
