from django.conf import settings
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils import timezone
import requests


class Services(models.Model):
    """Модель услуг медицинской компании"""

    name = models.CharField(max_length=200, verbose_name="Название услуги", help_text="Введите название услуги")
    description = models.TextField(verbose_name="Описание услуги", help_text="Введите описание услуги")
    price = models.IntegerField(verbose_name="Сумма оплаты за услугу")
    photo = models.ImageField(
        upload_to="services/", blank=True, null=True, help_text="Загрузите нужную фотографию услуги"
    )
    doctors = models.ForeignKey("Doctors", on_delete=models.CASCADE, verbose_name="Врач")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Content(models.Model):
    """Модель контента сайта"""

    name_content = models.CharField(
        max_length=100, verbose_name="Название контента", help_text="Введите название контента"
    )
    text_content = models.TextField(
        verbose_name="Текст контента", blank=True, null=True, help_text="Введите текст контента"
    )
    image_content = models.ImageField(
        upload_to="content/", blank=True, null=True, help_text="Загрузите нужную фотографию"
    )

    def __str__(self):
        return self.name_content

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ["name_content",]


class Doctors(models.Model):
    """Модель команды врачей с информацией о них для сайта"""

    first_name = models.CharField(max_length=100, verbose_name="Имя врача", help_text="Введите имя врача")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия врача", help_text="Введите фамилию врача")
    surname = models.CharField(max_length=100, verbose_name="Отчество врача", help_text="Введите отчество врача")
    photo_doctor = models.ImageField(
        upload_to="doctors/", blank=True, null=True, help_text="Загрузите нужную фотографию"
    )
    comment = models.TextField(verbose_name="Текст описания о враче", blank=True, null=True, help_text="Введите текст")
    specialization = models.CharField(max_length=255, verbose_name="Специализация")
    experience = models.PositiveIntegerField(default=0, verbose_name="Опыт работы (лет)")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.surname}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.surname or ''}"

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ["last_name", "first_name"]


class Contacts(models.Model):
    """Модель контактов компании"""

    name = models.CharField(max_length=250, verbose_name="Название компании", default='Diagnostic')
    address = models.TextField(verbose_name="Адрес компании", help_text="Введите адрес компании", default='Diagnostic')
    phone_company = models.CharField(
        max_length=15, verbose_name="Телефон компании", help_text="Введите телефон для связи", blank=True, null=True
    )
    head_physician = models.CharField(
        max_length=250, verbose_name="ФИО главврача компании", help_text="Введите ФИО главврача", blank=True, null=True
    )
    email_company = models.EmailField(
        unique=True, verbose_name="Электронная почта", help_text="Введите электронную почту компании", blank=True, null=True
    )
    legal_entity = models.CharField(
        max_length=250, verbose_name="Юридичесок лицо", help_text="Юридическое лицо представляющее компанию", blank=True, null=True
    )
    link_company = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на компанию")
    actual = models.BooleanField(
        default=True,
        verbose_name="Актуальность контактной информации о компании",
        help_text="Действующая ли информация",
    )
    latitude = models.FloatField(verbose_name="Широта (координата Y)")
    longitude = models.FloatField(verbose_name="Долгота (координата X)")

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self.geocode()  # Автоматически определяем координаты при сохранении
        super().save(*args, **kwargs)

    def geocode(self):
        """Получает координаты через Яндекс.Geocoder API"""

        if not self.address:
            return None

        # Формируем запрос к API
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": settings.YANDEX_GEOCODER_API_KEY,  # Ключ из настроек Django
            "geocode": self.address,
            "format": "json",
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            # Извлекаем координаты из ответа
            pos = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            self.longitude, self.latitude = map(float, pos.split())
            return True
        except Exception as e:
            print(f"Ошибка геокодирования: {e}")
            return False

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Appointment(models.Model):
    """Модель записи на примем"""

    STATUS_CHOICES = [
        ("pending", "Ожидает подтверждения"),
        ("confirmed", "Подтверждена"),
        ("completed", "Завершена"),
        ("cancelled", "Отменена"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="appointments"
    )
    service = models.ForeignKey(
        "Services", on_delete=models.CASCADE, verbose_name="Услуга", related_name="appointments"
    )
    appointment_date = models.DateTimeField(
        verbose_name="Дата и время приема",
        validators=[MinValueValidator(limit_value=timezone.now, message="Дата приема не может быть в прошлом")],
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус записи")
    notes = models.TextField(verbose_name="Дополнительные заметки", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"
        ordering = ["-appointment_date"]
        constraints = [models.UniqueConstraint(fields=["user", "appointment_date"], name="unique_user_appointment")]

    def __str__(self):
        return f"{self.user} - {self.service} ({self.appointment_date})"

    def is_upcoming(self):
        """Проверяет, является ли прием предстоящим"""

        return self.appointment_date > timezone.now() and self.status in ["pending", "confirmed"]

    def cancel(self):
        """Отменяет запись на прием"""

        if self.status != "completed":
            self.status = "cancelled"
            self.save()

    def confirm(self):
        """Подтверждает запись на прием"""

        if self.status == "pending":
            self.status = "confirmed"
            self.save()

    def complete(self):
        """Отмечает прием как завершенный"""

        if self.status == "confirmed":
            self.status = "completed"
            self.save()


class DiagnosticResults(models.Model):
    """Модель Результаты диагностики"""

    # Связь с пользователем, который прошел диагностику
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diagnostic_results",
        verbose_name="Пользователь",
    )

    # Связь с услугой, по которой проводилась диагностика
    service = models.ForeignKey(
        "Services", on_delete=models.CASCADE, related_name="diagnostic_results", verbose_name="Услуга"
    )

    # Врач, который проводил диагностику (может быть из модели Doctors)
    doctor = models.ForeignKey("Doctors", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Врач")

    # Дата и время проведения диагностики
    date_performed = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время проведения")

    # Файл с результатами (PDF, изображение и т.д.)
    result_file = models.FileField(
        upload_to="diagnostic_results/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "jpg", "jpeg", "png", "dicom"])],
        verbose_name="Файл с результатами",
    )

    # Заключение врача (текстовое поле)
    conclusion = models.TextField(blank=True, null=True, verbose_name="Заключение врача")

    # Дополнительные заметки
    notes = models.TextField(blank=True, null=True, verbose_name="Дополнительные заметки")

    def __str__(self):
        return f"Результат диагностики {self.user} по услуге {self.service} от {self.date_performed}"

    class Meta:
        verbose_name = "Результат диагностики"
        verbose_name_plural = "Результаты диагностики"
        ordering = ["-date_performed"]


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    is_processed = models.BooleanField(default=False, verbose_name='Обработано')

    def __str__(self):
        return f'Сообщение от {self.name} ({self.email})'

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'
        ordering = ['-created_at']
