from collections import namedtuple
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import homeview,ItemDetailView,signup,login,logout,add_to_cart,remove_from_cart,OrderSummary,remove_single_item_from_cart,Checkout,OrderedView,TotalOrderView,Productsview,payment,export_csv,delete_order,update_order,pdf_order,handlerequest

app_name="cart"
urlpatterns=[
    path('',homeview,name='home'),
    path('products',Productsview,name='products'),
    path('product/<slug>/',ItemDetailView.as_view(),name='product-detail'),
    path('add-to-cart/<slug>/',add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart,name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>',remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('order-summary/',OrderSummary.as_view(),name='order-summary'),
    path('ordered/',OrderedView.as_view(),name='ordered'),
    path('checkout/',Checkout.as_view(),name='checkout'),
    path('totalorder/',TotalOrderView.as_view(),name='totalorder'),
    path('payment',payment,name='payment'),
    path('updatedelivery/<slug>',delete_order,name="delete_order"),
    path('update_order/<slug>',update_order,name="update_order"),
    path('pdf_order/<slug>',pdf_order,name="pdf_order"),
    path('export_csv',export_csv,name='export-csv'),
    path('signup/',signup,name='signup'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('handlerequest/',handlerequest,name='handlerequest'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)