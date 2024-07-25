from django.contrib import admin
from .models import Supplier, Service

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_approved']
    list_filter = ['is_approved']
    search_fields = ['username', 'email']
    ordering = ['username']
    actions = ['approve_suppliers']

    def approve_suppliers(self, request, queryset):
        queryset.update(is_approved=True)
    approve_suppliers.short_description = "Approve selected suppliers"

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Service)
