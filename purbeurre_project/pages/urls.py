"""design URLs for an app."""
from django.urls import path

from .views import HomePageView, LegalNotices


urlpatterns = [
    path('legal/', LegalNotices.as_view(), name='legal'),
    path('', HomePageView.as_view(), name='home'),
]
