from django.contrib import admin
from seller_profile.models import SellerCategory,SellerProfileCreateAdmin,SellerProfileForUser#,SellerProfile,SellerProfileOption
# Register your models here.

admin.site.register(SellerCategory)
admin.site.register(SellerProfileCreateAdmin)
admin.site.register(SellerProfileForUser)
