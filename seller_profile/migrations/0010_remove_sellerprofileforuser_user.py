# Generated by Django 2.2 on 2020-10-25 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller_profile', '0009_sellerprofileforuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerprofileforuser',
            name='user',
        ),
    ]
