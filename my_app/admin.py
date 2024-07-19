from django.contrib import admin
from .models import Product, SavedCart
# Register your models here.

admin.site.register(Product)
admin.site.register(SavedCart)