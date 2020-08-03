from django.urls import path

from .views import ProductDetailView, SubstitutesListView

urlpatterns = [
    path('<slug:pk>', ProductDetailView.as_view(), name='book_detail'),
    path('substitutes/', SubstitutesListView.as_view(), name='substitutes'),
]
