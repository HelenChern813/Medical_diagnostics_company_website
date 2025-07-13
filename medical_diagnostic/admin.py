from django.contrib import admin
from django.utils.html import format_html

from .models import Appointment, Contacts, Content, DiagnosticResults, Doctors, Feedback, Services

admin.site.site_header = "Панель управления Medical Diagnostic"
admin.site.site_title = "Medical Diagnostic"
admin.site.index_title = "Администрирование сайта"


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "is_processed", "short_message")
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "message")
    list_editable = ("is_processed",)
    date_hierarchy = "created_at"
    actions = ["mark_as_processed", "mark_as_unprocessed"]
    readonly_fields = ("created_at",)

    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Краткое сообщение"

    @admin.action(description="Пометить как обработанное")
    def mark_as_processed(self, request, queryset):
        queryset.update(is_processed=True)

    @admin.action(description="Пометить как необработанное")
    def mark_as_unprocessed(self, request, queryset):
        queryset.update(is_processed=False)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "doctor_info", "photo_preview")
    list_filter = ("doctors",)
    search_fields = ("name", "description", "doctors__last_name")
    list_per_page = 20
    raw_id_fields = ("doctors",)
    autocomplete_fields = ["doctors"]

    def doctor_info(self, obj):
        return f"{obj.doctors.last_name} {obj.doctors.first_name}"

    doctor_info.short_description = "Врач"

    def photo_preview(self, obj):
        if obj.photo:
            from django.utils.html import format_html

            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "-"

    photo_preview.short_description = "Превью фото"


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
    list_display = ("full_name", "specialization", "experience", "photo_preview")
    list_filter = ("specialization", "experience")
    search_fields = ("last_name", "first_name", "specialization")
    readonly_fields = ("photo_preview",)
    fieldsets = (
        (None, {"fields": ("last_name", "first_name", "surname")}),
        ("Профессиональная информация", {"fields": ("specialization", "experience", "education", "qualification")}),
        ("Фотография", {"fields": ("photo_doctor", "photo_preview")}),
        ("Дополнительно", {"fields": ("comment", "schedule")}),
    )

    def photo_preview(self, obj):
        if obj.photo_doctor:
            from django.utils.html import format_html

            return format_html('<img src="{}" width="100" height="100" />', obj.photo_doctor.url)
        return "-"

    photo_preview.short_description = "Превью фото"


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
    list_display = ("user", "service", "doctor", "formatted_date", "status", "is_upcoming")
    list_filter = ("status", "appointment_date", "doctor")
    search_fields = ("user__email", "doctor__email", "service__name")
    list_editable = ("status",)
    date_hierarchy = "appointment_date"
    actions = ["send_reminders"]
    readonly_fields = ("created_at", "updated_at")

    def formatted_date(self, obj):
        return obj.appointment_date.strftime("%d.%m.%Y %H:%M")

    formatted_date.short_description = "Дата и время"
    formatted_date.admin_order_field = "appointment_date"

    def is_upcoming(self, obj):
        return obj.is_upcoming()

    is_upcoming.boolean = True
    is_upcoming.short_description = "Предстоящий?"


@admin.register(DiagnosticResults)
class DiagnosticResultsAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "doctor", "formatted_date", "file_link")
    list_filter = ("date_performed", "doctor", "service")
    search_fields = ("user__email", "doctor__email", "service__name")
    date_hierarchy = "date_performed"
    readonly_fields = ("date_performed", "file_preview")

    def formatted_date(self, obj):
        return obj.date_performed.strftime("%d.%m.%Y %H:%M")

    formatted_date.short_description = "Дата проведения"

    def file_link(self, obj):
        if obj.result_file:
            from django.utils.html import format_html

            return format_html('<a href="{}">Скачать</a>', obj.result_file.url)
        return "-"

    file_link.short_description = "Файл результатов"

    def file_preview(self, obj):
        if obj.result_file:
            if obj.result_file.name.endswith((".jpg", ".jpeg", ".png")):
                return format_html('<img src="{}" width="300" />', obj.result_file.url)
            return format_html('<a href="{}">Скачать файл</a>', obj.result_file.url)
        return "-"

    file_preview.short_description = "Превью файла"
