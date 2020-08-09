from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from autoslug import AutoSlugField

from users.models import CustomUser


class Category(models.Model):
    id_category = models.CharField(
        "id_category", max_length=150, primary_key=True)
    slug = AutoSlugField("id Category Adress",
                         unique=True,
                         always_update=False,
                         populate_from="id_category")
    name = models.CharField("url catégorie", max_length=255)
    products = models.IntegerField("Nb produits")
    url = models.CharField("url catégorie", max_length=255)
    visible = models.BooleanField("visible")

    def __str__(self):
        return self.name


class ProductManager(models.Manager):

    def search(self, name):
        queryset = self.get_queryset()
        try:
            products = queryset.filter(
                Q(product_name_fr__icontains=name)
                | Q(pk=name)
                | Q(generic_name_fr__icontains=name)
                | Q(brands__icontains=name)
                | Q(categories__name__icontains=name)
            ).order_by(
                '-popular'
            )
        except ObjectDoesNotExist:
            products = None
        finally:
            return products

    def get_substitutes(self, product):
        queryset = self.get_queryset()
        try:
            substitutes = queryset.filter(
                nutriscore_score__lte=product.nutriscore_score
            ).filter(
                categories__in=product.categories.all()
            ).exclude(
                pk=product.id_product
            ).order_by(
                'nutriscore_grade'
            )
        except ObjectDoesNotExist:
            substitutes = None
        finally:
            return substitutes


class Product(models.Model):

    NUTRISCORE_GRADE = [
        ('A', 'Score A'),
        ('B', 'Score B'),
        ('C', 'Score C'),
        ('D', 'Score D'),
        ('E', 'Score E'),
    ]
    # primary key
    id_product = models.CharField(
        "id_product", max_length=15, primary_key=True)
    # for product link
    slug = AutoSlugField("id Product Address",
                         unique=True,
                         always_update=False,
                         populate_from="id_product")
    # product informations
    product_name_fr = models.CharField("nom produit", max_length=150)
    nutriscore_score = models.IntegerField("score produit")
    nutriscore_grade = models.CharField("grade produit",
                                        max_length=1,
                                        choices=NUTRISCORE_GRADE)
    stores = models.CharField("magasins", max_length=255)
    generic_name_fr = models.TextField("description", blank=True)
    brands = models.CharField("marque", max_length=100)
    url_openfood = models.URLField("url product", default="#")
    popular = models.IntegerField("popularite", default=0)
    # images
    small_image = models.URLField("small image", default="#")
    display_image = models.URLField("display image", default="#")
    # nutriments
    is_beverage = models.BooleanField("Boisson", default=False)
    fat_100g = models.FloatField("Lipides", default=-1)
    satured_fat_100g = models.FloatField("Acides gras", default=-1)
    sugars_100g = models.FloatField("Sucres", default=-1)
    salt_100g = models.FloatField("Sel", default=-1)
    # category (relation many to many through CatProd)
    categories = models.ManyToManyField(Category, through='CatProd')
    favorites = models.ManyToManyField(CustomUser, through='Favorite')

    # Manager
    objects = ProductManager()

    def __str__(self):
        return self.product_name_fr

    def get_absolute_url(self):
        return reverse(
            'products:detail',
            kwargs={"slug": self.slug}
        )


class CatProd(models.Model):

    class Meta:
        unique_together = (('id_category', 'id_product'),)

    id_category = models.ForeignKey('Category', on_delete=models.CASCADE)
    id_product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Favorite(models.Model):

    class Meta:
        unique_together = (('id_user', 'id_product'),)

    id_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    id_product = models.ForeignKey('Product', on_delete=models.CASCADE)
