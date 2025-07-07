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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("moderator", "moderator"),
        ]
