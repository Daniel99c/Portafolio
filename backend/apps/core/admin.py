from django.contrib import admin

from .models import Certificate, Experience, ExperienceGroup, Fact, Profile, Project, ProjectDetail, StackGroup


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'updated_at')
    fieldsets = (
        ('Portada', {'fields': ('full_name', 'short_name', 'title', 'profession', 'location', 'summary', 'stack_line', 'badges', 'photo')}),
        ('Sobre mí', {'fields': ('bio', 'approach')}),
        ('Contacto', {'fields': ('email', 'github', 'linkedin', 'website')}),
        ('Hoja de vida', {'fields': ('cv', 'cv_download_name')}),
        ('Formación', {'fields': ('degree_title', 'degree_institution', 'degree_date', 'degree_honors', 'research_title', 'research_text')}),
    )

    # Hay un solo perfil
    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order')
    list_editable = ('order',)


@admin.register(StackGroup)
class StackGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'primary', 'order')
    list_editable = ('order',)


class ExperienceGroupInline(admin.StackedInline):
    model = ExperienceGroup
    extra = 0


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'period', 'current', 'published', 'order')
    list_editable = ('published', 'order')
    list_filter = ('published', 'current')
    inlines = [ExperienceGroupInline]


class ProjectDetailInline(admin.StackedInline):
    model = ProjectDetail
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published', 'order')
    list_editable = ('published', 'order')
    list_filter = ('published',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectDetailInline]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'type', 'year', 'public_file', 'featured', 'order')
    list_editable = ('public_file', 'featured', 'order')
    list_filter = ('type', 'public_file', 'featured', 'issuer')
    search_fields = ('title', 'issuer')
