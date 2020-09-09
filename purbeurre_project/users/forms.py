from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """fields for signup page."""
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class CustomUserChangeForm(UserChangeForm):
    """fields for update profil page."""
    password = None

    class Meta:
        model = get_user_model()
        fields = ('username', 'name', 'bio', )
