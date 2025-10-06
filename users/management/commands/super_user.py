from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Кастомная команда создания суперпользователя"""

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            User.objects.get(email="admin@exemple.com").delete()
        except ObjectDoesNotExist:
            pass
        user = User.objects.create(
            email="admin@exemple.com",
        )
        user.set_password("41234123Ww")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Успешно создан суперпользователь с email {user.email}"))
