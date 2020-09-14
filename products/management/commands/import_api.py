from django.core.management.base import BaseCommand
from django.core.management import call_command

import requests

from products.models import Product, Category
from django.conf import settings


class Command(BaseCommand):
    """command to import data from OpenFoodFacts products and categories are
    deleted before import."""
    help = """
            importation des données de l'api Openfoodcats
            et enregistrement dans la base de données.
        """

    def handle(self, *args, **kwargs):
        """main method."""
        self.stdout.write(self.style.WARNING(
            'Début de l\'importation API OpenFoodFacts'))

        # Remove data products
        call_command('delete_products')

        # request all categories from API
        contents = self.request_api_categories()

        # delete duplicates
        contents_unique = list({v['id']: v for v in contents['tags']}.values())

        # create list of Category to insert in bdd
        for category in contents_unique:
            if category['id'] in settings.CATEGORIES_VISIBLE:
                self.add_category(category)

                # import products from this category
                contents = self.request_api_products(category)
                # delete duplicates products in one category
                contents_unique = list(
                    {v['_id']: v for v in contents['products']}.values())

                for product in contents_unique:
                    self.add_product(product, category['id'])

    def request_api_categories(self):
        """return json data from category api."""
        url = "https://fr.openfoodfacts.org/categories&json=1"
        res = requests.get(url)
        self.stdout.write(self.style.WARNING(
            "Categories - Status code: %s" % res.status_code))
        return res.json()

    def request_api_products(self, category):
        """return json data products from one category."""
        url = "https://fr.openfoodfacts.org/cgi/search.pl? \
                    action=process& \
                    tagtype_0=categories& \
                    tag_contains_0=contains& \
                    tag_0=%s& \
                    sort_by=unique_scans_n& \
                    page_size=100& \
                    json=1& \
                    page=1" % (category['id'])
        res = requests.get(url.replace(" ", ""))
        self.stdout.write("Produits de %s - Status code: %s" % (
            category["name"],
            res.status_code))
        return res.json()

    def add_category(self, category):
        """add one category in database."""
        new_category = Category.objects.create(
            id_category=category['id'],
            name=category['name'],
            products=category['products'],
            url=category['url'],
            visible=True
        )
        new_category.save()

    def add_product(self, product, id_category):
        """add one product in database."""
        # Mandatory fields in the API
        mandatory_fields = [
            '_id',
            'product_name_fr',
            'nutriscore_score',
            'nutriscore_grade',
            'stores',
            'generic_name_fr',
            'brands',
            'url',
            'nutriments',
        ]

        if self.check_all_fields_product(product, mandatory_fields):
            new_product, created = Product.objects.get_or_create(
                # product informations
                id_product=str(product['_id']),
                product_name_fr=product['product_name_fr'],
                nutriscore_score=product['nutriscore_score'],
                nutriscore_grade=product['nutriscore_grade'].upper(),
                stores=product['stores'],
                generic_name_fr=product['generic_name_fr'],
                brands=product['brands'],
                url_openfood=product['url'],
                popular=product.get('unique_scans_n', 1),
                # images
                small_image=product.get('image_front_small_url', "#"),
                display_image=product.get('image_front_url', "#"),
                # nutriments
                is_beverage=product.get('is_beverage', False),
                fat_100g=product['nutriments'].get('fat_100g', -1),
                satured_fat_100g=product['nutriments'].get(
                    'saturated-fat_100g', -1),
                sugars_100g=product['nutriments'].get('sugars_100g', -1),
                salt_100g=product['nutriments'].get('salt_100g', -1)
            )
            if created:
                category = Category.objects.get(pk=id_category)
                new_product.categories.add(category)
                new_product.save()

    def check_all_fields_product(self, product, mandatory_fields):
        """checks if the mandatory fields are present in the dict product."""
        for field in mandatory_fields:
            if field not in product:
                return False
        return True
