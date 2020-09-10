"""design routes for users app."""

from django.urls import path
from .views import SignupPageView, UpdateUserPageView

urlpatterns = [
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('<pk>/profile/', UpdateUserPageView.as_view(), name='profile'),
]
