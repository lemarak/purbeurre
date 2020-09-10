"""Declaration of the users application."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Class called by settings.py for the registration of the users
    application."""
    name = 'users'
