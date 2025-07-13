# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /medical_diagnostic_company_website

# Копируем файл с зависимостями и устанавливаем их
COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
&& poetry install --no-interaction --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

RUN mkdir -p /medical_diagnostic_company_website/static
RUN mkdir -p /medical_diagnostic_company_website/media

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]