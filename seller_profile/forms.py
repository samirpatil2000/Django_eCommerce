from django import forms
from .models import SellerProfileForUser
from core.models import Item

class CreateSellerProfileForm(forms.ModelForm):
    class Meta:
        model=SellerProfileForUser
        fields=['name','seller_category']

class UpdateSellerProfileForm(forms.ModelForm):
    class Meta:
        model=SellerProfileForUser
        fields=['name','seller_category']

    def save(self, commit=True):
        shop=self.instance
        shop.name=self.cleaned_data['name']
        shop.seller_category=self.cleaned_data['seller_category']

        if commit:
            shop.save()
        return shop

class AddProductForm(forms.ModelForm):
    # sellerprofileshop=SellerProfileForUser.objects.filter(seller_profile__user=)
    class Meta:
        model=Item
        fields=['title','price','discount_price','category','brand','subcategory','desc','sellerprofileshop']
class AddProductFromShop(forms.ModelForm):
    class Meta:
        model=Item
        fields=['title','price','discount_price','category','brand','subcategory','desc']


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['title','price','discount_price','category','brand','subcategory','desc']

    def save(self, commit=True):
        product=self.instance
        product.title=self.cleaned_data['title']
        product.price=self.cleaned_data['price']
        product.discount_price=self.cleaned_data['discount_price']
        product.category=self.cleaned_data['category']
        product.brand=self.cleaned_data['brand']
        product.subcategory=self.cleaned_data['subcategory']
        product.desc=self.cleaned_data['desc']

        if commit:
            product.save()
        return product

