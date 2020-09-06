"""Managing admin pages for the products application."""


from django.contrib import admin

from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    """Managing admin pages for the products application."""
    list_display = ('product_name_fr', 'id_product', 'brands')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
