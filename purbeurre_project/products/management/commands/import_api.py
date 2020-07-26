from django.core.management.base import BaseCommand, CommandError

import requests

from products.models import Product, Category
from django.conf import settings
from ._private import add_category, add_product


class Command(BaseCommand):
    help = """
            importation des données de l'api Openfoodcats
            et enregistrement dans la base de données.
        """

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(
            'Début de l\'importation API OpenFoodFacts'))

        # Removes records from the category table
        self.stdout.write('Suppression des données Catégorie')
        Category.objects.all().delete()

        # Removes records from the product table
        self.stdout.write('Suppression des données Produit')
        Product.objects.all().delete()

        # request all categories from API
        res = requests.get('https://fr.openfoodfacts.org/categories.json')
        self.stdout.write(self.style.WARNING(
            "Categories - Status code: %s" % res.status_code))
        contents = res.json()

        # delete duplicates
        contents_unique = list({v['id']: v for v in contents['tags']}.values())

        # create list of Category to insert in bdd
        for category in contents_unique:
            if category['id'] in settings.CATEGORIES_VISIBLE:
                add_category(category)
