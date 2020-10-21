from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import SellerProfileForUser,SellerProfileCreateAdmin
from django.views.generic import CreateView,UpdateView
from .forms import CreateSellerProfileForm,AddProductForm,AddProductFromShop,UpdateProductForm
from core.models import Item
# Create your views here.


@login_required
def create_seller_profile_view(request):
    form = CreateSellerProfileForm(request.POST or None)
    seller_profile_from_admin=get_object_or_404(SellerProfileCreateAdmin,user=request.user)

    context={

    }
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.seller_profile=seller_profile_from_admin
            create_shop = form.save(commit=False)
            messages.info(request," You have successfully created your shop")
            create_shop.save()
            context['form']=form
            return redirect('seller_home')
    return render(request, 'seller_profile/create_seller_form.html', {'form': form})

@login_required
def seller_shops(request):
    shops=SellerProfileForUser.objects.filter(user=request.user)
    context={
        'shops':shops
    }
    return render(request,'seller_profile/seller_home.html',context)
def seller_dashbord(request):
    context={

    }

    return render(request,'seller_profile/seller_dashboard.html',context)


def seller_add_item(request):
    addproductform=AddProductForm(request.POST or None)
    #sellerprofile_shop=get_object_or_404(SellerProfileForUser,user=request.user)
    context={

    }
    if request.method =="POST":
        if addproductform.is_valid():
            #addproductform.instance.user = request.user
            #addproductform.instance.slug = request.user
            add_product=addproductform.save(commit=False)
            add_product.save()
            messages.info(request,'Product is added')
            return redirect('seller_home')
        context['addproductform'] = addproductform
    return render(request,'seller_profile/add_product_form.html' ,{'addproductform': addproductform})

# shop detail view for products
def shop_details_product(request,id):
    user_shop=get_object_or_404(SellerProfileForUser,id=id)
    user_products=Item.objects.filter(sellerprofileshop=user_shop)

    context={
        'shop':user_shop,
        'products':user_products
    }
    return render(request,'seller_profile/shop_detail_and_products.html',context)

#create product from shops
@login_required
def add_product_from_shop(request,id):
    seller_shop=get_object_or_404(SellerProfileForUser,id=id)
    addproductfromshopform=AddProductFromShop(request.POST or None)
    context={

    }
    if request.method=="POST":
        if addproductfromshopform.is_valid():
            add_product=addproductfromshopform.save(commit=False)
            addproductfromshopform.instance.sellerprofileshop=seller_shop
            add_product.save()
            messages.info(request,'Product is added')
            return redirect('seller_home')
    return render(request,'seller_profile/add_product_from_shop.html',{'addproductfromshopform':addproductfromshopform})

@login_required
def update_product_from_shop(request,slug):
    product=get_object_or_404(Item,slug=slug)
    seller_shop=product.sellerprofileshop
    if request.user != seller_shop.seller_profile.user:
        return HttpResponse("Restricted  ...!")
    if request.POST:
        updateProductForm=UpdateProductForm(request.POST or None,instance=product)
        if updateProductForm.is_valid():
            obj=updateProductForm.save(commit=False)
            obj.save()
            product=obj
            messages.info(request,f'{product.title} is updated')
            return redirect('product-detail',slug)
    form=UpdateProductForm(
        initial={
            "title":product.title ,
            "price":product.price ,
            "discount_price":product.discount_price ,
            "category":product.category ,
            "brand":product.brand ,
            "subcategory":product.subcategory ,
            "desc":product.desc ,
        }
    )
    context={
        'updateproductform':form,
    }
    return render(request,'seller_profile/edit_product_from_shop.html',context)

def delete_product(request,slug):
    product=get_object_or_404(Item,slug=slug)
    seller_shop=product.sellerprofileshop
    if request.user != seller_shop.seller_profile.user:
        return HttpResponse("Restricted  ...!")
    product.delete()
    return redirect('seller_home')
