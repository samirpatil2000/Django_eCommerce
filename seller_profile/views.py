from django.shortcuts import render,HttpResponse

# Create your views here.
def seller_home(request):
    context={

    }
    return render(request,"seller_profile/seller_home.html",context)