from django.urls import path
from django.views.generic import TemplateView

from medical_diagnostic.apps import MedicalDiagnosticConfig

from . import views

app_name = MedicalDiagnosticConfig.name

urlpatterns = [
    path("appointments_list/", views.AppointmentListView.as_view(), name="appointments_list"),
    path("appointments_create/", views.AppointmentCreateView.as_view(), name="appointments_create"),
    path("appointment/<int:pk>/", views.AppointmentDetailView.as_view(), name="appointment_detail"),
    path("appointment_update/<int:pk>/", views.AppointmentUpdateView.as_view(), name="appointment_update"),
    path("appointment_cancel/<int:pk>/", views.AppointmentCancelView.as_view(), name="appointment_cancel"),
    path("calendar/", views.appointment_calendar_view, name="calendar"),
    path("services_list/", views.ServicesListView.as_view(), name="services_list"),
    path("services/<int:pk>/", views.ServicesDetailView.as_view(), name="service_detail"),
    path("contact/", views.ContactsListView.as_view(), name="contact_detail"),
    path("directions_map/", views.directions_map, name="directions_map"),
    path("feedback/", views.feedback_view, name="feedback"),
    path("home_page/", TemplateView.as_view(template_name="home_page.html"), name="home_page"),
    path("about_company/", TemplateView.as_view(template_name="about_company.html"), name="about_company"),
]
