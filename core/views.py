from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect,reverse
from.models import Item,OrderItem,Order
from django.views.generic import ListView,DetailView
from django.utils import timezone
# Create your views here.
def index(request):
    context={
        'items':Item.objects.all()
    }
    return render(request,'core/home-page.html',context)

def Checkout(request):
    return render(request,'core/checkout-page.html')

def product(request):
    return render(request,'core/product-page.html')



class HomeView(ListView):
    model=Item
    template_name ='core/home-page.html'
    context_object_name = 'object_list'
    paginate_by = 3

"""the context in this case is change now it is not items any more now it is object_list"""


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product-page.html'
    context_object_name = 'object'

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    """  item , user , ordered these are the fields of that respective model """


    if order_qs.exists():
        order = order_qs[0]
        """ check if the order item is in the order """

        if order.items.filter(item__slug=item.slug).exists():
            """ if order item is already the the cart the add quantity +=1 """
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("product-detail" ,slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request, ' {} added to your cart'.format(item))
            return redirect("product-detail",slug=slug)
    else:
        ordered_date = timezone.now()
        # order=OrderItem()
        # order.user=request.user
        # order.ordered_date=ordered_date
        # order.save()
        # order.items.add(order_item)

        # order=OrderItem(user=request.user,ordered_date=ordered_date)
        # # order.user=request.user
        # # order.ordered_date=ordered_date
        # order.objects.items.add(order_item)
        # order.save()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "{} is added to your cart.".format(item))
        return redirect("product-detail",slug=slug)

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.warning(request, "{} was removed from your cart.".format(item))
            return redirect("product-detail", slug=slug)
        else:
            messages.warning(request,"{} was removed from your cart.".format(item))
            return redirect("product-detail", slug=slug)
    else:
        messages.warning(request, "You do not have an active order")
        return redirect("product-detail",slug=slug)
