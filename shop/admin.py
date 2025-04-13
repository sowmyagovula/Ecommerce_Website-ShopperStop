from django.contrib import admin
from .models import Shop_model


# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'brand', 'user']


admin.site.register(Shop_model, ShopAdmin)

