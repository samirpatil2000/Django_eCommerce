import random

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.shortcuts import render,reverse

# Create your models here.
from django.utils.text import slugify
from django_countries.fields import CountryField
from seller_profile.models import SellerProfileForUser

from mptt.models import MPTTModel,TreeForeignKey
from django.core.validators import MaxValueValidator,MinValueValidator


CATEGORY_CHOICES=(
    ('S', 'MAC'),
    ('SW', 'MAC PRO'),
    ('OW', 'IPHONE')
)
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

productName=['iPhone 5s','iPhone 6s','iPhone Se','MacBook Air','MacBook Pro',
             'Sumsung Galaxy J7','Sumsung Galaxy J5','Sumsung Galaxy J2','Sumsung Galaxy J1 ace','LG mobile',
             'Asus Rog','Asus L3T01','Blackberry T9','Hp envy','Hp envy T56']
def default_product_name():
    n=random.randrange(0,len(productName))
    return productName[n]

def default_cat():
    cat_list=['Mobile','Laptops','Tv','Headphone','Earphone','Watch']
    n=random.randrange(0,len(cat_list))
    return cat_list[n]

def default_brand():
    brand_list=['Apple','Samsung','Lenovo','Xiaomi','MotoRolla','Google Pixels','Boat','Beat','Asus','HP','Tagg']
    n=random.randrange(0,len(brand_list))
    return brand_list[n]

def default_sub_cat():
    sub_cat_list=['Android','iPhone','Windows','Windows 7','Windows 8','Window 10','Window 10 lean','CromeBook','Smart Watch']
    n=random.randrange(0,len(sub_cat_list))
    return sub_cat_list[n]


class Category(models.Model):
    name=models.CharField(max_length=100,default=default_cat,unique=True)
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name=models.CharField(max_length=100,unique=True,default=default_sub_cat)
    category=models.ManyToManyField(Category)
    def __str__(self):
        return self.name

class Brand(models.Model):
    name=models.CharField(max_length=100,default=default_brand,unique=True)
    def __str__(self):
        return self.name



class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'



class Payment(models.Model):
     stripe_charge_id = models.CharField(max_length=50)
     user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL, blank=True, null=True)
     amount = models.IntegerField()
     timestamp = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.user.username


# alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet = 'azsxdcfvgbqwertyhnmjuiklop'



def random_string_gen():
    n=random.randint(0,len(alphabet))
    m=random.randint(0,len(alphabet))
    str1=alphabet[n:n+5]
    str2=alphabet[m:m+6]
    if m==n:
        return random_string_gen
    random_string=f'{str1}-{str2}'
    return random_string


class Item(models.Model):
    title=models.CharField(max_length=100,default=default_product_name)
    price=models.IntegerField(default=random.randrange(15000,50000,1000))
    discount_price=models.IntegerField(blank=True,null=True)


    # TODO with choice field
    #category=models.CharField(choices=CATEGORY_CHOICES,max_length=2 ,null=True,blank=True)

    """  In template you have to use {{ i.get_category_display }}  ==> Shirt  If   {{ i.category }} ===> S """

    #label=models.CharField(choices=LABEL_CHOICES,default='P',max_length=1,null=True,blank=True)

    """  In template you have to use {{ i.get_label_display }}  ==> primary  If   {{ i.label }} ===> P """

    slug=models.SlugField(blank=True,null=True,unique=True)

    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    subcategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE,blank=True,null=True)


    desc=models.TextField(default="THis is desc ",max_length=500)
    favourite=models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     blank=True,null=True)
    # quantity=models.IntegerField(default=1)
    sellerprofileshop=models.ForeignKey(SellerProfileForUser,on_delete=models.CASCADE)

    random_string_gen_for_slug=models.CharField(default=random_string_gen,max_length=100)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail',kwargs={'slug':self.slug})

    def get_add_to_cart_url(self):
        return reverse('add_to_cart',kwargs={'slug':self.slug})
    #
    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart',kwargs={'slug':self.slug})

    def get_add_to_favourites_url(self):
        return reverse('add_to_favourite',kwargs={'slug':self.slug})

    def get_update_item_url(self):
        return reverse('update_product',kwargs={'slug':self.slug})

    def get_delete_item_url(self):
        return reverse('delete_product',kwargs={'slug':self.slug})



# TODO this is the slug field signal

def pre_save_slug(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=slugify(f'{instance.title}-{instance.random_string_gen_for_slug}')
pre_save.connect(pre_save_slug,sender=Item)


class Comment(MPTTModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent=TreeForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='children')
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    content = models.TextField(default="This is the comment")
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} {self.item.title}'

    class MPTTMeta:
        order_insertion_by = ['publish']

def default_review():
    n=random.randrange(0,6)
    return n

class Review(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    content = models.TextField(default="This is the comment")
    rate=models.IntegerField(default=default_review,
                             validators=[
                                 MinValueValidator(1),
                                 MaxValueValidator(5)
                                         ])

    def __str__(self):
        return f'{self.user.username}--{self.item.title}'


#  shopping cart
class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item}'

    def get_total_order_price(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.price:
            return self.get_total_order_price()
        return self.get_total_discount_price()



# this is your actual order
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    billing_address = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_amount(self):
        total=0
        for i in self.items.all():
            total+=i.get_final_price()
        return total


class FavouriteList(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item_name=models.ManyToManyField(Item)


    def __str__(self):
        return f'{self.user.username}'

class ProductViewByUser(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Item,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user} - {self.product}'