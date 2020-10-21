from django.db import models
from django.conf import settings
# Create your models here.
import random

from django.urls import reverse


def default_seller_Cat():
    seller_cat_list=['Electronics','Books','Home','Kitchen','Cloths and Merchandise']
    n=random.randrange(0,len(seller_cat_list))
    return seller_cat_list[n]

class SellerCategory(models.Model):
    name=models.CharField(max_length=100,default=default_seller_Cat)

    def __str__(self):
        return self.name


class SellerProfileCreateAdmin(models.Model):
    name=models.CharField(max_length=100,default="SellerProfileOption")
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name}'

class SellerProfileForUser(models.Model):
    name=models.CharField(max_length=100,default="Seller")
    seller_category=models.ForeignKey(SellerCategory,on_delete=models.CASCADE,blank=True,null=True)
    seller_profile=models.ForeignKey(SellerProfileCreateAdmin,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)


    def __str__(self):
        return f'{self.name} of {self.seller_profile.user.username}'

    def get_shop_absolute_url(self):
        return reverse('shop_details_product',kwargs={'id':self.pk})

