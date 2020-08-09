from django.urls import path

from .views import (
    ProductDetailView,
    SubstitutesListView,
    SearchListView,
    FavoritesListView,
    add_favorite)

urlpatterns = [
    path('<slug:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchListView.as_view(), name='search'),
    path('substitutes/<slug:pk>', SubstitutesListView.as_view(), name='substitutes'),
    path('add_favorite/<int:pk>/', add_favorite, name='add_favorite'),
    path('substitutes/favorites/', FavoritesListView.as_view(), name='favorites'),
]
