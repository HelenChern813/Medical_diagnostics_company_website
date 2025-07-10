from django import template

from medical_diagnostic.models import Contacts, Content, Doctors, Services

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
