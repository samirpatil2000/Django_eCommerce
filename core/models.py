from django.db import models
from django.conf import settings
from django.shortcuts import render,reverse

# Create your models here.

CATEGORY_CHOICES=(
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)



class Item(models.Model):
    title=models.CharField(max_length=100)
    price=models.FloatField()
    discount_price=models.FloatField(default=200)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2 ,null=True,blank=True)

    """  In template you have to use {{ i.get_category_display }}  ==> Shirt  If   {{ i.category }} ===> S """

    label=models.CharField(choices=LABEL_CHOICES,default='P',max_length=1,null=True,blank=True)

    """  In template you have to use {{ i.get_label_display }}  ==> primary  If   {{ i.label }} ===> P """

    slug=models.SlugField()
    desc=models.TextField(default="THis is desc ",max_length=500)
    # quantity=models.IntegerField(default=1)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail',kwargs={'slug':self.slug})

    def get_add_to_cart_url(self):
        return reverse('add_to_cart',kwargs={'slug':self.slug})
    #
    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart',kwargs={'slug':self.slug})


#  shopping cart
class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item}'

# this is your actual order
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()


    def __str__(self):
        return self.user.username

