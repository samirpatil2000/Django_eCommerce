from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import SellerProfileForUser,SellerProfileCreateAdmin
from django.views.generic import CreateView
from .forms import CreateSellerProfileForm
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