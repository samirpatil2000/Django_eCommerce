from django import forms
from .models import SellerProfileForUser

class CreateSellerProfileForm(forms.ModelForm):
    class Meta:
        model=SellerProfileForUser
        fields=['name','seller_category']
