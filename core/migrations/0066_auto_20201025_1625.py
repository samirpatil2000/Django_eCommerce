# Generated by Django 2.2 on 2020-10-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_auto_20201022_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=32000),
        ),
    ]
