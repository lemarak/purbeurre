"""takes a Web request and returns a Web response."""

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm


class SignupPageView(generic.CreateView):
    """Display signup page."""
    form_class = CustomUserCreationForm
    # providing a reversed URL to a decorator
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class UpdateUserPageView(LoginRequiredMixin, generic.UpdateView):
    """Display update page."""
    model = get_user_model()
    login_url = reverse_lazy('login')
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('home')
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        user = get_user_model()
        return user.objects.get(id=self.request.user.id)
