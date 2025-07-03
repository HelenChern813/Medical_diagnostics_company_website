from django.conf import settings
from django.db import models
from django.db.models import SET_NULL


class Services(models.Model):
    '''Модель услуг медицинской компании'''

    name = models.CharField(max_length=200, verbose_name='Название услуги', help_text='Введите название услуги')
    description = models.TextField(verbose_name='Описание услуги', help_text='Введите описание услуги')
    price = models.IntegerField(verbose_name="Сумма оплаты за услугу")
    foto = models.ImageField(upload_to="services/", blank=True, null=True,
                                      help_text='Загрузите нужную фотографию услуги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Content(models.Model):
    '''Модель контента сайта '''

    name_content = models.CharField(max_length=100, verbose_name='Название контента', help_text='Введите название контента')
    text_content = models.TextField(verbose_name='Текст контента', blank=True, null=True, help_text='Введите текст контента')
    image_content = models.ImageField(upload_to="content/", blank=True, null=True, help_text='Загрузите нужную фотографию')

    def __str__(self):
        return self.name_content

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"


class Doctors(models.Model):
    '''Модель команды врачей с информацией о них для сайта'''

    first_name = models.CharField(max_length=100, verbose_name='Имя врача', help_text='Введите имя врача')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия врача', help_text='Введите фамилию врача')
    surname = models.CharField(max_length=100, verbose_name='Отчество врача', help_text='Введите отчество врача')
    foto_doctor = models.ImageField(upload_to="doctors/", blank=True, null=True, help_text='Загрузите нужную фотографию')
    comment = models.TextField(verbose_name="Текст описания о враче", blank=True, null=True, help_text='Введите текст')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"


class Contacts(models.Model):
    '''Модель контактов компании'''

    address = models.CharField(max_length=250, verbose_name='Адрес компании', help_text='Введите адрес компании')
    phone_company = models.CharField(max_length=15, verbose_name='Телефон компании', help_text='Введите телефон для связи')
    head_physician = models.CharField(max_length=250, verbose_name='ФИО главврача компании', help_text='Введите ФИО главврача')
    email_company = models.EmailField(unique=True, verbose_name="Электронная почта", help_text='Введите электронную почту компании')
    legal_entity = models.CharField(max_length=250, verbose_name='Юридичесок лицо', help_text='Юридическое лицо представляющее компанию')
    link_company = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на компанию")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class AppointmentBooking(models.Model):
    '''Модель записи на прием'''

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, verbose_name='Пользователь')
    services = models.ForeignKey(Services, on_delete=SET_NULL, verbose_name='Услуга для записи')
