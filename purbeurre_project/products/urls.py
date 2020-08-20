from django.urls import path

from .views import (
    ProductDetailView,
    SubstitutesListView,
    SearchListView,
    FavoritesListView,
    admin_favorite
)

urlpatterns = [
    path('<slug:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('search/', SearchListView.as_view(), name='search'),
    path('substitutes/<slug:pk>', SubstitutesListView.as_view(),
         name='substitutes'),
    path('favorite/<int:pk>/<str:action>/', admin_favorite,
         name='admin_favorite'),
    path('substitutes/favorites/', FavoritesListView.as_view(),
         name='favorites'),
]
