from django.contrib import admin

from .models import Appointment, Contacts, Content, DiagnosticResults, Doctors, Feedback, Services


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_processed")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "message")
    list_editable = ("is_processed",)
    date_hierarchy = "created_at"


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "photo", "doctors")
    list_filter = ("name", "price", "doctors")
    search_fields = ("name", "price", "doctors", "description")


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "name_content", "text_content", "image_content")
    list_filter = (
        "name_content",
        "text_content",
    )
    search_fields = (
        "name_content",
        "text_content",
    )


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "surname")
    list_filter = (
        "first_name",
        "last_name",
    )
    search_fields = (
        "first_name",
        "last_name",
    )


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address")
    list_filter = (
        "name",
        "address",
    )
    search_fields = (
        "name",
        "address",
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "doctor", "service", "appointment_date", "status")
    list_filter = ("status", "doctor", "appointment_date")
    search_fields = ("user__username", "doctor__username", "service__name")
    raw_id_fields = ("user", "doctor", "service")


@admin.register(DiagnosticResults)
class DiagnosticResultsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "service", "doctor", "date_performed")
    list_filter = (
        "user",
        "service",
        "doctor",
        "date_performed",
    )
    search_fields = (
        "user",
        "service",
        "doctor",
        "date_performed",
    )
