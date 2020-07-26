from django.db import models
from django.urls import reverse
from django.conf import settings

from autoslug import AutoSlugField


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
        return id_category


class Product(models.Model):

    NUTRISCORE_GRADE = [
        ('A', 'Score A'),
        ('B', 'Score B'),
        ('C', 'Score C'),
        ('D', 'Score D'),
        ('E', 'Score E'),
    ]

    id_product = models.CharField(
        "id_product", max_length=15, primary_key=True)
    slug = AutoSlugField("id Product Address",
                         unique=True,
                         always_update=False,
                         populate_from="id_product")
    product_name_fr = models.CharField("nom produit", max_length=150)
    nutriscore_score = models.IntegerField("score produit")
    nutriscore_grade = models.CharField("grade produit",
                                        max_length=1,
                                        choices=NUTRISCORE_GRADE)
    stores = models.CharField("magasins", max_length=255)
    generic_name_fr = models.TextField("description", blank=True)
    brands = models.CharField("marque", max_length=100)
    category = models.ManyToManyField(Category, through='CatProd')

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
