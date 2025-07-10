from django import template
from medical_diagnostic.models import Content, Services, Contacts, Doctors

register = template.Library()


@register.simple_tag
def get_content():
    return Content.objects.all()


@register.simple_tag
def get_services():
    return Services.objects.all()


@register.simple_tag
def get_contacts():
    return Contacts.objects.all()


@register.simple_tag
def get_doctors():
    return Doctors.objects.all()
