from datetime import timedelta

from django.contrib import admin
from django.db.models import Count
from django.utils import timezone

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'kind', 'target')
    list_filter = ('kind', 'created_at')
    search_fields = ('target',)
    date_hierarchy = 'created_at'
    change_list_template = 'admin/analytics/event/change_list.html'

    # Solo lectura: los eventos los genera el sitio
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        labels = dict(Event.KINDS)
        now = timezone.now()

        def totals(since):
            rows = Event.objects.filter(created_at__gte=since).values('kind').annotate(total=Count('id'))
            counts = {row['kind']: row['total'] for row in rows}
            return [(labels[kind], counts.get(kind, 0)) for kind, _ in Event.KINDS]

        top = (
            Event.objects.filter(created_at__gte=now - timedelta(days=30))
            .exclude(target='')
            .values('kind', 'target')
            .annotate(total=Count('id'))
            .order_by('-total')[:10]
        )
        extra_context = {
            **(extra_context or {}),
            'summary': [
                ('Últimos 7 días', totals(now - timedelta(days=7))),
                ('Últimos 30 días', totals(now - timedelta(days=30))),
            ],
            'top': [{**row, 'kind': labels[row['kind']]} for row in top],
        }
        return super().changelist_view(request, extra_context)
