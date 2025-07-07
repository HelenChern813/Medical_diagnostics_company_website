from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render
from django.urls import reverse_lazy


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
