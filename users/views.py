import secrets

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from users.forms import CustomUserCreationForm, ProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    template_name = "register.html"
    success_url = reverse_lazy("medical_diagnostic:home_page")
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        """Оправка письма с токкеном"""

        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке для подверждения почты: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждение почты"""

    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class PasswordResetUserView(PasswordResetView):
    """Восстановление пароля"""

    template_name = "reset_password.html"
    email_template_name = "password_reset_email.html"
    from_email = settings.DEFAULT_FROM_EMAIL
    success_url = reverse_lazy("users:password_reset_done")
    subject_template_name = "password_reset_subject.txt"


def logout_view(request):
    logout(request)
    return redirect("/")


class ProfilePageView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile.html"
    context_object_name = "user"

    def get_context_data(self, *args, **kwargs):
        context = super(ProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User, id=self.kwargs["pk"])
        context["page_user"] = page_user
        return context


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user and not request.user.is_staff:
            raise PermissionDenied("У вас нет прав для редактирования этого профиля")
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "profile_form.html"
    success_url = reverse_lazy("users:profile")
