from django.contrib import admin
from mystore.models import Product, UserProfileInfo, OrderItem, Order

# Register your models here.

admin.site.register(Product)
admin.site.register(UserProfileInfo)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstName', 'lastName', 'email', 'address', 'created', 'updated']
    inlines = [OrderItemInline]

    
admin.site.register(Order, OrderAdmin)
