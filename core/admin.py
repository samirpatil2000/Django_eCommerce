from django.contrib import admin
from.models import Item,OrderItem,Order,Payment,BillingAddress,FavouriteList,Category,SubCategory,Brand,ProductViewByUser,Comment,Review
# Register your models here.
from mptt.admin import MPTTModelAdmin

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(BillingAddress)
admin.site.register(FavouriteList)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(ProductViewByUser)


admin.site.register(Review)


admin.site.register(Comment,MPTTModelAdmin)

