from django.contrib.auth.views import (LoginView, PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordResetDoneView)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import (PasswordResetUserView, ProfilePageView, ProfileUpdateView, RegisterView, email_verification,
                         logout_view)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("reset_password/", PasswordResetUserView.as_view(), name="reset_password"),
    path(
        "reset_password/done/",
        PasswordResetDoneView.as_view(template_name="reset_password_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="reset_password_confirm.html", success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("confirm/<str:token>/", email_verification, name="email_confirm"),
    path("users_profile/<int:pk>/", ProfilePageView.as_view(), name="profile"),
    path("profile_edit/<int:pk>/", ProfileUpdateView.as_view(), name="profile_edit"),
]
