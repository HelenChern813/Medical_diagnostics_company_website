# 🏥 Сайт компании медицинской диагностики- Django проект

![Django](https://img.shields.io/badge/Django-5.2.4-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17+-blue)
![Python](https://img.shields.io/badge/Python-3.12%2B-yellow)
![Poetry](https://img.shields.io/badge/Poetry--orange )
## 📋 Описание проекта

Веб-приложение для медицинского диагностического центра с полным циклом работы:
- Записи пациентов
- Управление медицинскими услугами
- Диагностика и результаты
- Управление персоналом

### 🧩 Основные модули

| Приложение          | Функционал                                                                 |
|---------------------|---------------------------------------------------------------------------|
| `medical_diagnostic`| Основной функционал: записи, услуги, диагностика, врачи, обратная связь  |
| `users`             | Управление пользователями: регистрация, аутентификация, профили          |

## ✨ Ключевые возможности

### 👨‍⚕️ Для пациентов
- 📝 Онлайн-запись на прием
- 📅 Управление своими записями
- 📊 Просмотр результатов анализов
- ✉️ Система обратной связи

### 👨‍⚕️ Для врачей
- 👥 Управление приемами
- ✅ Подтверждение записей
- 📁 Добавление результатов диагностики

### 🛠 Административные функции
- ⚙️ Полное управление услугами
- 👨‍⚕️ Управление врачами
- 📍 Контактная информация клиники
- 🔍 Просмотр всех записей и результатов

## 🏗 Структура проекта
``` 
Medical_diagnostics_company_website/
├── config/               # Django main settings
├── medical_diagnostic/   # Main application
├── users/                # User management app
├── .env.example          # Environment example
├── pyproject.toml        # Poetry configuration
├── README.md             # Documentation
└── manage.py             # Entry point
```
## Приложение `users`
### 📦 Основные модели

```python
class User(AbstractUser):
    # Доп. поля:
    phone_number = models.CharField()  # Телефон
    avatar = models.ImageField()       # Фото профиля
    is_doctors = models.BooleanField() # Флаг врача
    # ... и другие поля
```
## 🏥 Приложение medical_diagnostic

Ядро системы с полным функционалом медицинского центра. Реализовано как отдельное Django-приложение с расширенной бизнес-логикой.

### 🧩 Основные модели

#### Модели данных

| Модель              | Описание                          | Особенности |
|---------------------|----------------------------------|------------|
| `Services`         | Медицинские услуги клиники      | Привязка к врачам, ценам и фото |
| `Doctors`          | Расширенная информация о врачах | Специализация, образование, расписание |
| `Appointment`      | Система записи пациентов        | 4 статуса записи, валидация дат |
| `DiagnosticResults`| Результаты обследований         | Поддержка PDF/изображений, заключение врача |
| `Contacts`         | Контакты клиники с геоданными   | Автоматическое геокодирование через Yandex API |


## 🚀 Установка и запуск

### Предварительные требования
- Python 3.12+
- PostgreSQL 17+
- Poetry 

**Клонирование репозитория:**
   ```bash
   git clone https://github.com/HelenChern813/Medical_diagnostics_company_website.git
   cd Medical_diagnostics_company_website
```
**Активируйте виртуальное окружение и установите зависимости:**
   ```bash
poetry shell
poetry update
```
**Создайте файл .env с нужными конфигурациями для проекта по шаблону .env.example**
```
# Core settings
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=medical_db
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=localhost
DB_PORT=5432

# Email service
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your@yandex.ru
EMAIL_HOST_PASSWORD=app-password
DEFAULT_FROM_EMAIL=your@yandex.ru

# API keys
YANDEX_GEOCODER_API_KEY=your-api-key
```
**Применение миграций:**
   ```bash
python manage.py migrate
```

**Создание суперпользователя:**
   ```bash
python manage.py super_user  
```

**Запуск сервера:**
   ```bash
python manage.py runserver

```


## 🛠  Дополнительные команды

| Command                                   | Description          |  |
|-------------------------------------------|----------------------|--|
| poetry add package                        | Добавить зависимость | 📝 |
| poetry run python manage.py collectstatic | Сбор статики         | 📝 |
| poetry run python manage.py super_user    | Создать админа       | 📝 |

## 🛠 Технологии
### Backend
- Django 5.2.4 - основной фреймворк

- Django REST Framework - API эндпоинты

- DRF SimpleJWT - JWT аутентификация

- Poetry - управление зависимостями

### База данных
- PostgreSQL - основное хранилище данных

- psycopg2 - адаптер для работы с PostgreSQL

### Дополнительно
- Yandex SMTP - отправка почты

- Yandex Geocoder API - работа с картами

- Django Debug Toolbar - отладка (только для разработки)

<div align="center"> <sub>Разработано с ❤️ для медицинских учреждений</sub> </div> 






