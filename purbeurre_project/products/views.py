from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Product, Favorite
from users.models import CustomUser


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/detail.html'


class SubstitutesListView(ListView):
    # context_object_name = 'substitutes
    template_name = 'products/substitutes.html'
    context_object_name = 'substitutes'
    paginate_by = 6

    def get_queryset(self):
        product = Product.objects.get(pk=self.kwargs['pk'])
        substitutes = Product.objects.get_substitutes(product)
        if substitutes:
            return substitutes
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs['pk'])
        context['selected_product'] = product
        return context


class SearchListView(ListView):
    template_name = 'products/search.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET['search']
        products = Product.objects.search(query)
        if products:
            return products
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET['search']
        return context


class FavoritesListView(ListView):
    template_name = 'products/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(
            CustomUser,
            id=self.request.user.id
        )
        favorites = Product.objects.filter(favorites=user)
        # favorites = Product.objects.get_favorites(user)
        return favorites


def add_favorite(request, pk):
    """Save substitute in favorites."""
    if request.user.is_authenticated:

        user = get_object_or_404(
            CustomUser,
            id=request.user.id
        )

        substitute = get_object_or_404(
            Product,
            pk=pk
        )

        Favorite.objects.update_or_create(
            id_user=user,
            id_product=substitute)

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('sign_up')
