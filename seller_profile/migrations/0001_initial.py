# Generated by Django 2.2 on 2020-10-19 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import seller_profile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=seller_profile.models.default_seller_Cat, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SellerProfileOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='SellerProfileOption', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Seller', max_length=100)),
                ('seller_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seller_profile.SellerCategory')),
                ('seller_profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seller_profile.SellerProfileOption')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
