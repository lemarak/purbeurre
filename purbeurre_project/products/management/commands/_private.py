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


def add_product(product):
    pass
