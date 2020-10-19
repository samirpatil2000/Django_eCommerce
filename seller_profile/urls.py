
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
   # path('',HomeView.as_view(),name='index'),
   path('',views.seller_shops,name='seller_home'),
   path('create/',views.create_seller_profile_view,name='seller_profile_create')

]