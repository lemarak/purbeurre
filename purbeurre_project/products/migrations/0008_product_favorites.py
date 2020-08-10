# Generated by Django 3.0.8 on 2020-08-09 16:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0007_product_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorites',
            field=models.ManyToManyField(through='products.Favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]