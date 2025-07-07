from django.urls import path
from . import views
from medical_diagnostic.apps import MedicalDiagnosticConfig

app_name = MedicalDiagnosticConfig.name

urlpatterns = [
    path('appointments_list/', views.AppointmentListView.as_view(), name='appointments_list'),
    path('appointments_create/', views.AppointmentCreateView.as_view(), name='appointments_create'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointments_detail'),
    path('appointments_update/<int:pk>/', views.AppointmentUpdateView.as_view(), name='appointments_update'),
    path('appointments_cancel/<int:pk>/', views.AppointmentCancelView.as_view(), name='appointments_cancel'),
    path('calendar/', views.appointment_calendar_view, name='calendar'),
]