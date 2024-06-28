from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product, Cart

class CartAdmin(admin.ModelAdmin):
    def get_cart_items(self, obj):
        return " | ".join([f"'{p.product_id.product_name}' : '{p.quantity}'" for p in obj.items.all()])
    def total_quantity(self, obj):
        return sum([p.quantity for p in obj.items.all()])
    def total_price(self, obj):
        return round(sum([(p.product_id.price * p.quantity) for p in obj.items.all()]),2)
    list_display = ("user", "get_cart_items", "total_quantity", "total_price")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "category", "price")

class ReadOnlyUserAdmin(BaseUserAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ReadOnlyUserAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
admin.site.unregister(User)
admin.site.register(User, ReadOnlyUserAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Product, ProductAdmin)