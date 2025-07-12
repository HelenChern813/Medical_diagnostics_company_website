from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Appointment, DiagnosticResults, Feedback

User = get_user_model()


class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(is_doctors=True), to_field_name="last_name", label="Врач", required=True
    )

    class Meta:
        model = Appointment
        fields = ["doctor", "service", "appointment_date", "notes"]
        widgets = {
            "appointment_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["appointment_date"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data["appointment_date"]

        if appointment_date < timezone.now():
            raise forms.ValidationError("Нельзя записаться на прошедшую дату!")

        return appointment_date


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
        labels = {
            "name": "Ваше имя",
            "email": "Email для ответа",
            "phone": "Контактный телефон",
            "message": "Ваше сообщение",
        }


class DiagnosticResultsForm(forms.ModelForm):
    class Meta:
        model = DiagnosticResults
        fields = ["service", "doctor", "result_file", "conclusion", "notes"]
        widgets = {
            "conclusion": forms.Textarea(attrs={"rows": 4}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }
        labels = {
            "service": "Услуга",
            "doctor": "Врач",
            "result_file": "Файл с результатами",
            "conclusion": "Заключение врача",
            "notes": "Дополнительные заметки",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields["result_file"].widget.attrs.update({"class": "form-control-file"})
