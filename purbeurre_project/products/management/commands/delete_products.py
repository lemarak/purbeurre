"""delete categories and product in db."""
from django.core.management.base import BaseCommand

from products.models import Product, Category


class Command(BaseCommand):
    """delete categories and product in db."""
    def handle(self, *args, **kwargs):
        # Removes records from the category table
        self.stdout.write('Suppression des données Catégorie')
        Category.objects.all().delete()

        # Removes records from the product table
        self.stdout.write('Suppression des données Produit')
        Product.objects.all().delete()
