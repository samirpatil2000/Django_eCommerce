
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from. import views
from.views import HomeView,ItemDetailView

urlpatterns = [
   path('',HomeView.as_view(),name='index'),
   path('checkouts/',views.Checkout,name='checkouts'),
   path('product/<slug>',ItemDetailView.as_view(),name='product-detail'),
]