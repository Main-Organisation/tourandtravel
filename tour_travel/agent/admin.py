from django.contrib import admin
from .models import Agent, Booking
# Register your models here.

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['id', 'agent_username', 'agent_code', 'is_verify']
    list_display_links = ['id', 'agent_username']
    list_filter = ['is_verify']
    search_fields = [
        'user__username',
        'email',
        'agent_code'
    ]
    actions = ['mark_verify', 'mark_unverify']

    def agent_username(self, obj):
        return obj.user.username
    agent_username.short_description = 'agent_username'

    @admin.action(description="Mark as verify selected Agents")
    def mark_verify(self, request, queryset):
        queryset.update(is_verify=True)

    @admin.action(description="Mark as unverify selected Agents")
    def mark_unverify(self, request, queryset):
        queryset.update(is_verify=False)


admin.site.register(Booking)