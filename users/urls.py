from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import RegisterView, PasswordResetUserView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="catalog:product_list"), name="logout"),
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
]