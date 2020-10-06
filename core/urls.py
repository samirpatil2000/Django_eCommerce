
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
   path('add_to_cart/<slug>', views.add_to_cart, name='add_to_cart'),
   path('remove_from_cart/<slug>', views.remove_from_cart, name='remove_from_cart'),

]