from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product, Cart
import csv 
from django.http import HttpResponse

def download_order_history(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_history.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username', 'Product Name', 'Category', 'Price', 'Quantity', 'Order ID', 'Order Date'])
    for user in queryset:
        order = getattr(user, 'order', None)
        if order:
            for order_i in order.all():
                for item in order_i.order_items.all():
                    writer.writerow([
                        user.username,
                        item.product_id.product_name,
                        item.product_id.category,
                        item.product_id.price,
                        item.quantity,
                        order_i.id,
                        order_i.date
                    ])
    return response

download_order_history.short_description = "Download User's Order History"

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
    actions = [download_order_history]
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

