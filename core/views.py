from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views.generic.base import View

from.models import Item,OrderItem,Order,BillingAddress,Payment,FavouriteList,Category,SubCategory,Brand,ProductViewByUser
from django.views.generic import ListView,DetailView
from django.utils import timezone




import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from .forms import CheckoutForm
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
    template_name ='aws/index.html'
    context_object_name = 'object_list'
    paginate_by = 4

"""the context in this case is change now it is not items any more now it is object_list"""


def home_view(request):
    feature_product=Item.objects.all()[0:3]

    #TODO add hre history of user

    inspire_history_product=Item.objects.all()
    template_name ='aws/index.html'

    history_items=ProductViewByUser.objects.filter(user=request.user)


    # Create a paginator to split your products queryset
    paginator = Paginator(inspire_history_product, 1)  # Show 25 contacts per page
    # Get the current page number
    page = request.GET.get('page')
    # Get the current slice (page) of products
    inspire_history_product_paginator = paginator.get_page(page)
    try:
        paginated_queryset=paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset=paginator.page(1)
    except EmptyPage: # showing last page
        paginated_queryset=paginator.page(paginator.num_pages)

    context={
        'queryset': paginated_queryset,
        'feature_product':feature_product,
        'inspire_product':inspire_history_product_paginator,
        'history':history_items,
    }
    return render(request,template_name,context)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product-page.html'
    context_object_name = 'object'


class TestItemDetailView(DetailView):
    model = Item
    template_name = 'aws/single-product.html'
    context_object_name = 'object'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            product = self.kwargs['slug']
            product_id=product.pk
            ProductViewByUser.objects.get_or_create(user=request.user,product=product_id)

def product_detail_view(request,slug):
    item = get_object_or_404(Item, slug=slug)
    template_name = 'aws/single-product.html'

    if request.user.is_authenticated:
        ProductViewByUser.objects.get_or_create(user=request.user,product=item)

    context={
        'object':item
    }
    return render(request,template_name,context)




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
            messages.info(request,'{} added to your cart'.format(item))
            return redirect("product-detail",slug=slug)
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


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'aws/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('test_index')

class TestOrderSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            context={
                'object':order
            }
            return redirect(self.request,'aws/cart.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('test_index')

@login_required
def remove_single_item_from_cart(request, slug):
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

            """ THIS IS FOR ID QUANTITY  is become zero in order_summary then remove product form the cart  """
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)


            messages.warning(request, "{} was removed from your cart.".format(item))
            return redirect("order_summary")
        else:
            messages.warning(request,"{} was removed from your cart.".format(item))
            return redirect("order_summary")
    else:
        messages.warning(request, " Your Cart is updated ")
        return redirect("order_summary")

@login_required
def add_single_item_from_cart(request, slug):
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
            messages.warning(request, "{} was added from your cart.".format(item))
            return redirect("order_summary")
        else:
            order.items.add(order_item)
            messages.warning(request, "{} was added from your cart.".format(item))
            return redirect("order_summary")
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
        messages.warning(request, "{} was added from your cart.".format(item))
        return redirect("order_summary")

class CheckoutView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form=CheckoutForm()
        order=Order.objects.get(user=self.request.user,ordered=False)

        context={
            'order':order,
            'form':form
        }
        return render(self.request,'aws/checkout.html',context)

    def post(self,*args,**kwargs):
        form=CheckoutForm(self.request.POST or None)

        try:
            order=Order.objects.get(user=self.request.user)
            print(self.request.POST)
            if form.is_valid():
                shipping_address = form.cleaned_data.get('shipping_address')
                home_address = form.cleaned_data.get('home_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')

                # TODO: we have to more functionality to this field
                # save_billing_address = form.cleaned_data.get['save_billing_address']
                # save_info = form.cleaned_data.get['save_info']

                """ if user select the payment option then we will redirect it to that specific payment option)"""
                payment_option = form.cleaned_data.get('payment_option')

                """ here we are taking input from user and save this into the billing address model """

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=shipping_address,
                    apartment_address=home_address,
                    country=country,
                    zip=zip,
                )

                """ Here we are saving this in the Billing Address Model"""
                billing_address.save()

                """ Now here we are saving this billing address in the order model """
                order.billing_address=billing_address
                order.save()



                if payment_option == 'S':
                    return redirect('payment', payment_option='Stripe')   # TODO: here in redirect payment_option is  similiar to slug field
                elif payment_option == 'P':
                    return redirect('payment', payment_option='PayTm')
                elif payment_option =='GP':
                    return redirect('payment',payment_option='GooglePay')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('checkouts')
        except ObjectDoesNotExist:
            messages.warning(self.request," User doesn't have any address ")
            return redirect('order_summary')


        messages.info(self.request, 'Failed To Checkout')
        return redirect('checkouts')

class PaymentView(View):
    def get(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
             'order': order
         }
        return render(self.request,'core/payment.html',context)
    def post(self,*args,**kwargs):
        order=Order.objects.filter(user=self.request.user,ordered=False)
        token=self.request.POST.get('stripToken')
        amount = int(order.get_total())


        """ This is the api of stripe payment method """
        try:
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )


            # create Payment

            """ Now here we are adding data to the payment model payment model"""
            payment=Payment()
            payment.stripe_charge_id=charge['id']
            payment.user=self.request.user
            payment.amount=amount
            """ And here we are saving the payment data in the Payment model"""
            payment.save()


            order.ordered=True

            """Add payment data to the Order model Also"""
            order.payment=payment
            order.save()

            messages.success(self.request,"Your Oder Has Been Confirm")
            return redirect('/')

        except stripe.error.CardError as e:
             body = e.json_body
             err = body.get('error', {})
             messages.error(self.request, f"{err.get('message')}")
             return redirect("/")

        except stripe.error.RateLimitError as e:
             # Too many requests made to the API too quickly
             messages.error(self.request, "Rate limit error")
             return redirect("/")

        except stripe.error.InvalidRequestError as e:
             # Invalid parameters were supplied to Stripe's API
             messages.error(self.request, "Invalid parameters")
             return redirect("/")

        except stripe.error.AuthenticationError as e:
             # Authentication with Stripe's API failed
             # (maybe you changed API keys recently)
             messages.error(self.request, "Not authenticated")
             return redirect("/")

        except stripe.error.APIConnectionError as e:
             # Network communication with Stripe failed
             messages.error(self.request, "Network error")
             return redirect("/")

        except stripe.error.StripeError as e:
             # Display a very generic error to the user, and maybe send
             # yourself an email
             messages.error(
                 self.request, "Something went wrong. You were not charged. Please try again.")
             return redirect("/")

        except Exception as e:
             # send an email to ourselves
             messages.error(
                 self.request, "A serious error occurred. We have been notifed.")
             return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")

def templatingTesting(request):
    return render(request,'aws/index.html',{})

def contact(request):
    return render(request,'aws/contact.html',{})


# TODO add to favourite is done using model field not by Different Model

@login_required
def add_to_favourite(request,slug):
    item = get_object_or_404(Item, slug=slug)

    qs=Item.objects.filter(favourite=request.user)
    if qs.exists():
        messages.warning(request," You already added it ")
        return redirect('product-detail', slug=slug)
    else:
        item.favourite.add(request.user)
        messages.info(request," Product is added to favourite ")

    # return redirect('product-detail',slug=slug)



    """if qs.exists():
        messages.warning(request,"YOU already added it to the list ")
        return redirect('product-detail', slug=slug)

    else:
        items=Item.objects.filter(slug=slug)
        fav_item=FavouriteList.objects.create(user=request.user)
        fav_item.item_name.add(items)

        # favourite_item.item_name.set(items)

        "" set method id user because of create method is not use for MANYTOMANY Field ""

        # favourite_item.save()"""


    return redirect('product-detail', slug=slug)
@login_required
def remove_from_fav(request,slug):
    item = get_object_or_404(Item, slug=slug)
    qs=Item.objects.filter(favourite=request.user)
    if qs.exists():
        item.favourite.remove(request.user)
        messages.warning(request,f"successfully remove {item.title} ")
        return redirect('product-detail', slug=slug)
    else:
        messages.info(request," You don't have this product in your cart ")
        return redirect('product-detail', slug=slug)




@login_required
def yourFavListView(request):
    #favList=FavouriteList.objects.filter(user=request.user)
    favList=Item.objects.filter(favourite=request.user)
    context={
        'object_list':favList,
    }
    return render(request,'aws/indexFav.html',context)


"""class FavListView(LoginRequiredMixin,View):
    # model = FavouriteList
    template_name = 'core/index.html'
    # context_object_name = 'object_list'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context={
            'object_list':FavouriteList.objects.get(user=self.request.user)

        }
        return redirect(self.request,self.template_name,context)
    def get(self, *args, **kwargs):
        try:
            order = FavouriteList.objects.get(user=self.request.user)
            context = {
                'object': order
            }
            return render(self.request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('test_index')
"""


def is_valid_name(para):
    return para!='' and para is not None
def shopCategory(request):
    template_name='aws/category.html'

    obj=Item.objects.all()
    counter=Item.objects.all().count()


    cat=Category.objects.all()
    brand=Brand.objects.all()
    subCat=SubCategory.objects.all()

    category_name=request.GET.get('category')
    sub_category_name=request.GET.get('subcategory')
    brand_name=request.GET.get('brand')

    if is_valid_name(category_name) and category_name != 'Category':
        obj=obj.filter(category__name=category_name)
        counter=obj.filter(category__name=category_name).count()


    if is_valid_name(brand_name) and brand_name != 'Brand':
        obj=obj.filter(brand__name=brand_name)
        counter=obj.filter(brand__name=brand_name).count()

    if is_valid_name(sub_category_name) and sub_category_name !='SubCategory':
        obj=obj.filter(subcategory__name=sub_category_name)
        counter=obj.filter(subcategory__name=sub_category_name).count()



    context={
        'count':counter,
        'object':obj,
        'categories':cat,
        'subcategories':subCat,
        'brands':brand,
    }
    return render(request,template_name,context)

@login_required
def test_function_with_index(request):
    items=ProductViewByUser.objects.filter(user=request.user)
    context={
        'object_list':items
    }
    return render(request,'core/index.html',context)