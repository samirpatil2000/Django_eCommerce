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

"""the context in this case is change now it is not items any more now it is object_list"""


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product-page.html'
    context_object_name = 'object'

