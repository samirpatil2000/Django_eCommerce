
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from. import views
from.views import HomeView,ItemDetailView,OrderSummaryView,CheckoutView,PaymentView,TestIndex,TestItemDetailView,TestOrderSummaryView#,FavListView

urlpatterns = [
   path('',HomeView.as_view(),name='index'),
   path('checkouts/',CheckoutView.as_view(),name='checkouts'),
   #path('product/<slug>',ItemDetailView.as_view(),name='product-detail'),
   path('product/<slug>',TestItemDetailView.as_view(),name='product-detail'),
   path('add_to_cart/<slug>', views.add_to_cart, name='add_to_cart'),
   path('remove_from_cart/<slug>', views.remove_from_cart, name='remove_from_cart'),
   path('remove_single_item_from_cart/<slug>', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
   path('add_single_item_from_cart/<slug>', views.add_single_item_from_cart, name='add_single_item_from_cart'),
   path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
   path('payment/<payment_option>', PaymentView.as_view(), name='payment'),

   path('test/',TestIndex.as_view(),name='test_index'),
   path('test_product/<slug>',TestItemDetailView.as_view(),name='test-product-detail'),
   path('test_order_summary/', TestOrderSummaryView.as_view(), name='test_order_summary'),
   path('contact/',views.contact,name='contact'),

   # TODO  Favourite List

   path('add_to_favourite/<slug>',views.add_to_favourite,name='add_to_favourite'),
   path('remove_from_fav/<slug>',views.remove_from_fav,name='remove_from_fav'),
   path('favList/',views.yourFavListView,name='FavList'),
  # path('favList/',FavListView.as_view(),name='FavList')
   path('shop-category/',views.shopCategory,name='shop-category'),

]