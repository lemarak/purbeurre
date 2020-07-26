from django.core.management.base import BaseCommand, CommandError

from products.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Removes records from the category table
        self.stdout.write('Suppression des données Catégorie')
        Category.objects.all().delete()

        # Removes records from the product table
        self.stdout.write('Suppression des données Produit')
        Product.objects.all().delete()
