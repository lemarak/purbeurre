from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.db.models import Q

from .models import Product


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/detail.html'


class SubstitutesListView(ListView):
    model = Product
    # context_object_name = 'substitutes'
    template_name = 'products/substitutes.html'

    # def get_queryset(self):
    #     query = self.request.GET.get('search')
    #     product = Product.objects.find(query)
    #     context['product'] = product
    #     if product:
    #         substitutes = Product.objects.get_substitutes(product[0])
    #         context['substitutes'] = substitutes
    #         return substitutes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('search')
        product = Product.objects.find(query)
        context['product_select'] = product[0]
        if product:
            substitutes = Product.objects.get_substitutes(product[0])
            context['substitutes'] = substitutes
            print("context:", context)
        return context

