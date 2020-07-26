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
    mandatory_fields = [
        '_id',
        'product_name_fr',
        'nutriscore_score',
        'nutriscore_grade',
        'stores',
        'generic_name_fr',
        'brands',
    ]

    if check_all_fields_product(product, mandatory_fields):
        new_product = Product.objects.create(
            id_product=str(product['_id']),
            product_name_fr=product['product_name_fr'],
            nutriscore_score=product['nutriscore_score'],
            nutriscore_grade=product['nutriscore_grade'].upper(),
            stores=product['stores'],
            generic_name_fr=product['generic_name_fr'],
            brands=product['brands'],
        )
        category = Category.objects.get(pk=id_category)
        new_product.category.add(category)
        new_product.save()


def check_all_fields_product(product, mandatory_fields):
    for field in mandatory_fields:
        if field not in product:
            return False
            print(field)
    return True
