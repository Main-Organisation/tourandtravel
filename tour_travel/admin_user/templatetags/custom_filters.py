# custom_filters.py

from django import template

register = template.Library()

@register.filter
def has_service(supplier, service_name):
    return supplier.services.filter(name=service_name).exists()
