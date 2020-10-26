
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from. import views
from .views import UpdateProductForm

urlpatterns = [
   # path('',HomeView.as_view(),name='index'),
   path('',views.seller_shops,name='seller_home'),
   path('create/',views.create_seller_profile_view,name='seller_profile_create'),
   path('dashboard/',views.seller_dashbord,name='seller_dashboard'),
   path('add_product/',views.seller_add_item,name='add_product'),
   path('add_product_from_shop/<id>',views.add_product_from_shop,name='add_product_from_shop'),
   path('shop_detail/<id>',views.shop_details_product,name='shop_details_product'),
   path('shop_edit/<id>',views.update_seller_profile_view,name='shop_edit'),
   path('shop_delete/<id>',views.delete_seller_shop,name='shop_delete'),
   path('update_product/<slug>',views.update_product_from_shop,name='update_product'),
   path('delete_product/<slug>',views.delete_product,name='delete_product'),
   path('seller_all_products/', views.seller_all_products, name='seller_all_products')

]