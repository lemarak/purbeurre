from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Product


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/detail.html'


class SubstitutesListView(ListView):
    # context_object_name = 'substitutes
    template_name = 'products/substitutes.html'
    context_object_name = 'substitutes'

    def get_queryset(self):
        product = Product.objects.get(pk=self.kwargs['pk'])
        substitutes = Product.objects.get_substitutes(product)
        self.paginate_by = 6

        return substitutes

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

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET['search']

        return context


class FavoritesListView(ListView):
    template_name = 'products/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 6

    def get_queryset(self):
        favorites = Product.objects.filter(
            favorites=self.request.user
        ).order_by('-products_favorite.date_favorite')
        return favorites


def admin_favorite(request, pk, action='add'):
    """Save substitute in favorites."""
    if request.user.is_authenticated:

        substitute = get_object_or_404(
            Product,
            pk=pk
        )

        if action == 'add':
            substitute.favorites.add(request.user)
        elif action == 'del':
            substitute.favorites.remove(request.user)

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('sign_up')
