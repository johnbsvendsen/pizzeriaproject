from django.contrib import admin
from .models import Topping, Pizza, Drink, Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 
    readonly_fields = ('price_at_purchase',)
    fields = ('pizza', 'drink', 'size', 'quantity', 'selected_toppings', 'price_at_purchase')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'is_completed')
    list_filter = ('is_completed', 'created_at', 'user')
    search_fields = ('user__username', 'id')
    list_editable = ('is_completed',) 
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'total_price') 

admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Drink)
admin.site.register(Order, OrderAdmin)

