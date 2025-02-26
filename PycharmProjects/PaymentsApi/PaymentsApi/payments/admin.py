from django.contrib import admin
from .models import Item, Order

class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price")
    search_fields = ("name",)
    list_filter = ("price",)
    ordering = ("id",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "paid", "get_total_price")
    filter_horizontal = ("items",)

    def get_total_price(self, obj):
        return obj.total_price  # Доступ к @property
    get_total_price.short_description = "Total Price"

admin.site.register(Item, ItemAdmin)
