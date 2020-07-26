from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

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

        # Remove data products
        call_command('delete_products')

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

                # import products from this category
                str_requests = "https://fr.openfoodfacts.org/cgi/search.pl? \
                    action=process& \
                    tagtype_0=categories& \
                    tag_contains_0=contains& \
                    tag_0=%s& \
                    sort_by=unique_scans_n& \
                    page_size=20& \
                    json=1& \
                    page=1" % (category['id'])

                res = requests.get(str_requests.replace(" ", ""))
                self.stdout.write("Produits de %s - Status code: %s" % (
                    category["name"],
                    res.status_code))

                contents = res.json()
                # delete duplicates products in one category
                contents_unique = list(
                    {v['_id']: v for v in contents['products']}.values())

                for product in contents_unique:
                    add_product(product, category['id'])
