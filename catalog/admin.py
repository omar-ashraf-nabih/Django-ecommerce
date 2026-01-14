from django.contrib import admin
from .models import Product, ProductDiscountTier

class ProductDiscountTierInline(admin.TabularInline):
    model = ProductDiscountTier
    extra = 1
    fields = ("min_qty", "percent_off", "is_active")
    ordering = ("min_qty",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductDiscountTierInline]
