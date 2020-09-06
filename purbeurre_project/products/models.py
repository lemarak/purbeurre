"""Description of the database tables associated with products, each model maps
to a single database table."""

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from autoslug import AutoSlugField

from users.models import CustomUser


class Category(models.Model):
    """Stores a category."""
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
        """Custom representation of a category instance."""
        return str(self.name)


class ProductManager(models.Manager):
    """Methods associated with the Product model (find products and get
    substitutes)"""

    def search(self, name):
        """searches for products corresponding to parameter xxx."""
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
            products = queryset.none()
        finally:
            return products

    def get_substitutes(self, product):
        """obtain the substitutes of the product passed in parameter."""
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
            substitutes = queryset.none()
        finally:
            return substitutes


class Product(models.Model):
    """Stores a product."""
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
    product_name_fr = models.CharField("nom produit", max_length=255)
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
        """Custom representation of a product instance."""
        return str(self.product_name_fr)

    def get_absolute_url(self):
        """get url page from a product."""
        return reverse(
            'product_detail',
            args=[self.slug]
        )


class CatProd(models.Model):
    """
    Stores a category for a product, related to :model:`products.Product` and
    :model:`products.Category`.
    """
    class Meta:
        """for primary key."""
        unique_together = (('id_category', 'id_product'),)

    id_category = models.ForeignKey('Category', on_delete=models.CASCADE)
    id_product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Favorite(models.Model):
    """
    Stores a favourite for a product, related to :model:`products.Product` and
    :model:`auth.User`.
    """
    class Meta:
        """for primary key and ordering."""
        unique_together = (('id_user', 'id_product'),)
        ordering = ['-date_favorite']

    id_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    id_product = models.ForeignKey('Product', on_delete=models.CASCADE)
    date_favorite = models.DateTimeField('date favori', auto_now_add=True)
