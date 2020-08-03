from products.models import Product, Category


def add_category(category):
    new_category = Category.objects.create(
        id_category=category['id'],
        name=category['name'],
        products=category['products'],
        url=category['url'],
        visible=True
    )
    new_category.save()


def add_product(product, id_category):
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

    if check_all_fields_product(product, mandatory_fields):
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


def check_all_fields_product(product, mandatory_fields):
    for field in mandatory_fields:
        if field not in product:
            return False
    return True
