from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AppointmentForm, FeedbackForm
from .models import Appointment, Contacts, DiagnosticResults, Doctors, Services


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "appointments/appointment_list.html"
    context_object_name = "appointments"
    paginate_by = 10

    def get_queryset(self):
        # Показываем только записи текущего пользователя
        return Appointment.objects.filter(user=self.request.user).order_by("-appointment_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = "appointments/appointment_detail.html"
    context_object_name = "appointment"

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("medical_diagnostic:appointments_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/appointment_form.html"
    success_url = reverse_lazy("medical_diagnostic:appointments_list")

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Запись на прием успешно обновлена!")
        return response


class AppointmentCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

        if appointment.status == "completed":
            messages.error(request, "Нельзя отменить завершенную запись!")
        else:
            appointment.cancel()
            messages.success(request, "Запись успешно отменена!")

        return redirect("medical_diagnostic:appointments_list")


class ServicesListView(LoginRequiredMixin, ListView):
    model = Services
    template_name = "services_list.html"
    context_object_name = "services"


class ServicesDetailView(LoginRequiredMixin, DetailView):
    model = Services
    template_name = "services_detail.html"
    context_object_name = "service"


class ContactsListView(LoginRequiredMixin, ListView):
    model = Contacts
    template_name = "contacts_detail.html"
    context_object_name = "contacts"


def directions_map(request):
    company = Contacts.objects.first()
    context = {
        "company": company,
    }
    return render(request, "contacts.html", context)


def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()

            # Отправка email администратору
            send_mail(
                "Новое сообщение обратной связи",
                f"Получено новое сообщение от {feedback.name} ({feedback.email}).\n\n"
                f"Сообщение: {feedback.message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.")
            return redirect("medical_diagnostic:home_page")
    else:
        form = FeedbackForm()

    return render(request, "feedback_form.html", {"form": form})


class DiagnosticResultsListView(LoginRequiredMixin, ListView):
    model = DiagnosticResults
    template_name = "diagnostic_results_list.html"
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return DiagnosticResults.objects.all().order_by("-date_performed")
        return DiagnosticResults.objects.filter(user=self.request.user).order_by("-date_performed")


class DiagnosticResultsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = DiagnosticResults
    template_name = "diagnostic_results_detail.html"
    context_object_name = "result"

    def test_func(self):
        result = self.get_object()
        return self.request.user == result.user or self.request.user.is_staff


class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_doctors


class DoctorsDetailView(LoginRequiredMixin, DetailView):
    model = Doctors
    template_name = "doctors_detail.html"
    context_object_name = "doctors"


class DoctorAppointmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = "doctor_appointments.html"
    context_object_name = "appointments"

    def test_func(self):
        return self.request.user.is_doctors

    def get_queryset(self):
        # Показываем записи без врача или где текущий врач назначен
        return Appointment.objects.filter(Q(doctor=None) | Q(doctor=self.request.user)).order_by("-appointment_date")

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса для назначения врача и подтверждения записи"""

        appointment_id = request.POST.get("appointment_id")
        if not appointment_id:
            messages.error(request, "Не указана запись для подтверждения")
            return redirect("medical_diagnostic:doctor_appointments")

        appointment = get_object_or_404(Appointment, pk=appointment_id)

        # Назначаем врача и подтверждаем запись
        if appointment.doctor is None:
            appointment.doctor = request.user
            appointment.status = "confirmed"  # Автоматически подтверждаем
            appointment.save()

            # Отправляем уведомление пациенту
            send_mail(
                "Ваша запись подтверждена",
                f"Доктор {request.user.get_full_name()} подтвердил вашу запись "
                f'на {appointment.appointment_date.strftime("%d.%m.%Y в %H:%M")}',
                settings.DEFAULT_FROM_EMAIL,
                [appointment.user.email],
                fail_silently=False,
            )
            messages.success(request, "Вы успешно назначены на запись и она подтверждена")
        else:
            messages.warning(request, "Эта запись уже имеет назначенного врача")

        return redirect("medical_diagnostic:doctor_appointments")
