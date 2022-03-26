from django.contrib import admin
from .models import Items,Order,OrderItem,TotalOrder,Category,UserOtp,BillingAddress

# Register your models here.

admin.site.register(Items)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(BillingAddress)
