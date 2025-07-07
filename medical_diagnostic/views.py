from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AppointmentForm
from .models import Appointment, Doctors


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
        response = super().form_valid(form)
        messages.success(self.request, "Запись на прием успешно создана!")
        return response


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


def appointment_calendar_view(request):
    """Календарь записей (для врачей и пациентов)"""

    appointments = Appointment.objects.filter(user=request.user, appointment_date__gte=timezone.now())

    return render(
        request,
        "appointments/calendar.html",
        {
            "appointments": appointments,
        },
    )
