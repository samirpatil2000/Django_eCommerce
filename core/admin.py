from django.contrib import admin
from.models import Item,OrderItem,Order,Payment,BillingAddress
# Register your models here.

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(BillingAddress)
