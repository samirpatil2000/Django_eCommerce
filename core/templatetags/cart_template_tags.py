from django import template

from core.models import Order

register = template.Library()  # this registering your template


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs_cart=Order.objects.filter(user=user,ordered=False)   # ordered is false because we are not shwingthem their previus ordered items
        if qs_cart.exists():
            return qs_cart[0].items.count()
    return 0



