from django import forms
from .models import SellerProfileForUser
from core.models import Item

class CreateSellerProfileForm(forms.ModelForm):
    class Meta:
        model=SellerProfileForUser
        fields=['name','seller_category']

class AddProductFrom(forms.ModelForm):
    # sellerprofileshop=SellerProfileForUser.objects.filter(seller_profile__user=)
    class Meta:
        model=Item
        fields=['title','price','discount_price','category','brand','subcategory','desc','sellerprofileshop']

