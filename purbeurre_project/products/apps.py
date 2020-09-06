"""Declaration of the products application."""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Class called by settings.py for the registration of the products
    application."""
    name = 'products'
