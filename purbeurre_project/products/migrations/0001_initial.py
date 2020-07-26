# Generated by Django 3.0.8 on 2020-07-26 09:52

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id_category', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='id_category')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='id_category', unique=True, verbose_name='id Category Adress')),
                ('products', models.IntegerField(verbose_name='Nb produits')),
                ('url', models.CharField(max_length=255, verbose_name='url catégorie')),
                ('visible', models.BooleanField(verbose_name='visible')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id_product', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='id_product')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='id_product', unique=True, verbose_name='id Product Address')),
                ('product_name_fr', models.CharField(max_length=150, verbose_name='nom produit')),
                ('nutriscore_score', models.IntegerField(verbose_name='score produit')),
                ('nutriscore_grade', models.CharField(choices=[('A', 'Score A'), ('B', 'Score B'), ('C', 'Score C'), ('D', 'Score D'), ('E', 'Score E')], max_length=1, verbose_name='grade produit')),
                ('stores', models.CharField(max_length=255, verbose_name='magasins')),
                ('generic_name_fr', models.TextField(blank=True, verbose_name='description')),
                ('brands', models.CharField(max_length=100, verbose_name='marque')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('id_user', 'id_product')},
            },
        ),
        migrations.CreateModel(
            name='CatProd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
                ('id_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'unique_together': {('id_category', 'id_product')},
            },
        ),
    ]
