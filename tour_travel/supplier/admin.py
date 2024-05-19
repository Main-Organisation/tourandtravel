from django.contrib import admin
from .models import Service, Supplier

# Register your models here.

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier_username', 'supplier_code', 'is_verify', 'is_reject']
    list_display_links = ['id', 'supplier_username']
    list_filter = ['is_verify', 'is_reject']
    search_fields = [
        'user__username',
        'email',
        'supplier_code'
    ]
    # actions = ['mark_verify', 'mark_unverify']

    def supplier_username(self, obj):
        return obj.user.username
    supplier_username.short_description = 'supplier_username'

admin.site.register(Service)