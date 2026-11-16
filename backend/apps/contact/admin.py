from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'read', 'email_sent')
    list_filter = ('read', 'created_at')
    search_fields = ('name', 'email', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at', 'email_sent')
    fields = ('name', 'email', 'phone', 'message', 'created_at', 'email_sent', 'read')
    actions = ['mark_read', 'mark_unread']

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Abrir un mensaje lo marca como leído
        ContactMessage.objects.filter(pk=object_id, read=False).update(read=True)
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.action(description='Marcar como leídos')
    def mark_read(self, request, queryset):
        queryset.update(read=True)

    @admin.action(description='Marcar como no leídos')
    def mark_unread(self, request, queryset):
        queryset.update(read=False)
