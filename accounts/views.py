from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, ProfileForm
from .models import CustomUser

class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = "Your account has been created successfully. You can now log in."

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("dashboard")
    success_message = "Your profile has been updated."

    def get_object(self, queryset=None):
        return self.request.user
