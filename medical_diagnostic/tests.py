from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from medical_diagnostic.models import (
    Services,
    Appointment,
    DiagnosticResults,
    Feedback,
)
from users.models import User


class ServicesAPITestCase(APITestCase):
    """Тестирование API для услуг"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="doctor@test.com",
            password="testpass123",
            is_doctors=True,
        )
        self.service = Services.objects.create(
            name="Консультация",
            description="Первичная консультация",
            price=2000,
            doctors=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_service(self):
        """Тестирование создания услуги"""
        url = reverse("medical_diagnostic:services_list")
        data = {
            "name": "УЗИ",
            "description": "Ультразвуковое исследование",
            "price": 3500,
            "doctors": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Services.objects.count(), 2)

    def test_list_services(self):
        """Тестирование списка услуг"""
        url = reverse("medical_diagnostic:services_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Консультация")

    def test_retrieve_service(self):
        """Тестирование получения конкретной услуги"""
        url = reverse("medical_diagnostic:service_detail", args=[self.service.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Консультация")

    def test_update_service(self):
        """Тестирование обновления услуги"""
        url = reverse("medical_diagnostic:service_detail", args=[self.service.pk])
        data = {"price": 2500}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], 2500)

    def test_delete_service(self):
        """Тестирование удаления услуги"""
        url = reverse("medical_diagnostic:service_detail", args=[self.service.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Services.objects.count(), 0)


class AppointmentAPITestCase(APITestCase):
    """Тестирование API для записей на прием"""

    def setUp(self):
        self.doctor = User.objects.create_user(
            email="doctor@test.com",
            password="testpass123",
            is_doctors=True,
        )
        self.patient = User.objects.create_user(
            email="patient@test.com",
            password="testpass123",
        )
        self.service = Services.objects.create(
            name="Консультация",
            description="Первичная консультация",
            price=2000,
            doctors=self.doctor,
        )
        self.appointment = Appointment.objects.create(
            user=self.patient,
            doctor=self.doctor,
            service=self.service,
            appointment_date="2023-12-31T10:00:00Z",
            status="pending",
        )
        self.client.force_authenticate(user=self.patient)

    def test_create_appointment(self):
        """Тестирование создания записи на прием"""
        url = reverse("medical_diagnostic:appointments_create")
        data = {
            "doctor": self.doctor.id,
            "service": self.service.id,
            "appointment_date": "2023-12-31T11:00:00Z",
            "notes": "Тестовая запись",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_list_appointments(self):
        """Тестирование списка записей на прием"""
        url = reverse("medical_diagnostic:appointments_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "pending")

    def test_retrieve_appointment(self):
        """Тестирование получения конкретной записи"""
        url = reverse("medical_diagnostic:appointment_detail", args=[self.appointment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["service"], self.service.id)

    def test_update_appointment(self):
        """Тестирование обновления записи"""
        url = reverse("medical_diagnostic:appointment_update", args=[self.appointment.pk])
        data = {"notes": "Обновленные заметки"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["notes"], "Обновленные заметки")

    def test_cancel_appointment(self):
        """Тестирование отмены записи"""
        url = reverse("medical_diagnostic:appointment_cancel", args=[self.appointment.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        updated_appointment = Appointment.objects.get(pk=self.appointment.pk)
        self.assertEqual(updated_appointment.status, "cancelled")


class DoctorAppointmentAPITestCase(APITestCase):
    """Тестирование API для врачей (подтверждение записей)"""

    def setUp(self):
        self.doctor = User.objects.create_user(
            email="doctor@test.com",
            password="testpass123",
            is_doctors=True,
        )
        self.patient = User.objects.create_user(
            email="patient@test.com",
            password="testpass123",
        )
        self.service = Services.objects.create(
            name="Консультация",
            description="Первичная консультация",
            price=2000,
            doctors=self.doctor,
        )
        self.appointment = Appointment.objects.create(
            user=self.patient,
            doctor=self.doctor,
            service=self.service,
            appointment_date="2023-12-31T10:00:00Z",
            status="pending",
        )
        self.client.force_authenticate(user=self.doctor)

    def test_confirm_appointment(self):
        """Тестирование подтверждения записи врачом"""
        url = reverse("medical_diagnostic:confirm_appointment", args=[self.appointment.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        updated_appointment = Appointment.objects.get(pk=self.appointment.pk)
        self.assertEqual(updated_appointment.status, "confirmed")

    def test_doctor_appointments_list(self):
        """Тестирование списка записей врача"""
        url = reverse("medical_diagnostic:doctor_appointments")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["doctor"], self.doctor.id)


class DiagnosticResultsAPITestCase(APITestCase):
    """Тестирование API для результатов диагностики"""

    def setUp(self):
        self.doctor = User.objects.create_user(
            email="doctor@test.com",
            password="testpass123",
            is_doctors=True,
        )
        self.patient = User.objects.create_user(
            email="patient@test.com",
            password="testpass123",
        )
        self.service = Services.objects.create(
            name="Консультация",
            description="Первичная консультация",
            price=2000,
            doctors=self.doctor,
        )
        self.result = DiagnosticResults.objects.create(
            user=self.patient,
            service=self.service,
            doctor=self.doctor,
            conclusion="Тестовое заключение",
        )
        self.client.force_authenticate(user=self.patient)

    def test_list_diagnostic_results(self):
        """Тестирование списка результатов диагностики"""
        url = reverse("medical_diagnostic:diagnostic_results_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["conclusion"], "Тестовое заключение")

    def test_retrieve_diagnostic_result(self):
        """Тестирование получения конкретного результата"""
        url = reverse("medical_diagnostic:diagnostic_results_detail", args=[self.result.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["conclusion"], "Тестовое заключение")


class FeedbackAPITestCase(APITestCase):
    """Тестирование API для обратной связи"""

    def setUp(self):
        self.feedback = Feedback.objects.create(
            name="Тестовый пользователь",
            email="test@example.com",
            message="Тестовое сообщение",
        )

    def test_create_feedback(self):
        """Тестирование создания отзыва"""
        url = reverse("medical_diagnostic:feedback")
        data = {
            "name": "Новый пользователь",
            "email": "new@example.com",
            "message": "Новое сообщение",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Feedback.objects.count(), 2)
