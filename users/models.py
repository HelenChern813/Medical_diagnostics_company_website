from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    phone_number = models.CharField(max_length=15, verbose_name="Телефон пользователя", blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Токен")
    is_doctors = models.BooleanField(
        default=False, verbose_name="Аккаунт врача", help_text="Является ли пользователь врачем", blank=True, null=True
    )
    first_name = models.CharField(max_length=100, verbose_name="Имя", help_text="Введите имя", blank=True, null=True)
    last_name = models.CharField(
        max_length=100, verbose_name="Фамилия", help_text="Введите фамилию", blank=True, null=True
    )
    surname = models.CharField(
        max_length=100, verbose_name="Отчество", help_text="Введите отчество", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("moderator", "moderator"),
        ]
