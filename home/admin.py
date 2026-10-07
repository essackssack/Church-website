from django.contrib import admin

from .models import (
    AboutPage,
    BranchPage,
    CommunityPage,
    ContactPage,
    EventPage,
    HomePage,
    MagazinePage,
    MediaPage,
    MusicPage,
    SectionContent,
)


admin.site.site_header = 'CSI ST THOMAS CHURCH, SAMBAVARVADAKARAI Admin'
admin.site.site_title = 'CSI ST THOMAS CHURCH, SAMBAVARVADAKARAI Admin'
admin.site.index_title = 'Dashboard'


class ChurchModelAdminMixin:
    class Media:
        css = {
            'all': ('css/admin.css',),
        }


@admin.register(HomePage)
class HomePageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    fieldsets = (
        ('Overview', {'fields': ('title', 'subtitle', 'description', 'hero_image', 'is_active')}),
    )


@admin.register(AboutPage)
class AboutPageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'summary')
    fieldsets = (
        ('About', {'fields': ('title', 'summary', 'body', 'image', 'is_active')}),
    )


@admin.register(BranchPage)
class BranchPageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'location', 'pastor_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'location', 'address', 'pastor_name')
    fieldsets = (
        ('Branch Information', {'fields': ('name', 'location', 'address', 'pastor_name', 'description', 'is_active')}),
    )


@admin.register(EventPage)
class EventPageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'start_datetime', 'location', 'is_published')
    list_filter = ('is_published', 'start_datetime')
    search_fields = ('title', 'location', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-start_datetime',)
    fieldsets = (
        ('Event Details', {'fields': ('title', 'slug', 'description', 'image', 'start_datetime', 'end_datetime', 'location', 'is_published')}),
    )


@admin.register(MagazinePage)
class MagazinePageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'year', 'month', 'is_published')
    list_filter = ('is_published', 'year')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Magazine', {'fields': ('title', 'slug', 'description', 'month', 'year', 'cover_image', 'pdf_file', 'is_published', 'published_at')}),
    )


@admin.register(MusicPage)
class MusicPageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Music', {'fields': ('title', 'slug', 'description', 'audio_url', 'image', 'is_published')}),
    )


@admin.register(MediaPage)
class MediaPageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'media_type', 'is_published')
    list_filter = ('media_type', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Media', {'fields': ('title', 'slug', 'description', 'media_type', 'external_url', 'image', 'is_published')}),
    )


@admin.register(CommunityPage)
class CommunityPageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'body')
    fieldsets = (
        ('Community Content', {'fields': ('title', 'category', 'body', 'is_published')}),
    )


@admin.register(ContactPage)
class ContactPageAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'email', 'phone', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'email', 'address')
    fieldsets = (
        ('Contact Information', {'fields': ('title', 'phone', 'email', 'address', 'map_url', 'is_active')}),
    )


@admin.register(SectionContent)
class SectionContentAdmin(ChurchModelAdminMixin, admin.ModelAdmin):
    list_display = ('main_heading', 'subheading', 'title', 'is_published', 'updated_at')
    list_filter = ('main_heading', 'is_published')
    search_fields = ('main_heading', 'subheading', 'title', 'summary', 'body')
    list_per_page = 50
    fieldsets = (
        ('Existing Heading', {'fields': ('main_heading', 'subheading')}),
        ('Content', {'fields': ('title', 'summary', 'body', 'image', 'media_url')}),
        ('Optional Details', {'fields': ('event_date', 'location')}),
        ('Publication', {'fields': ('is_published',)}),
    )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        for field_name in ('main_heading', 'subheading'):
            value = request.GET.get(field_name)
            if value:
                initial[field_name] = value
        return initial

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['subheading_groups'] = [
            {
                'main_heading': main_heading,
                'subheadings': subheadings,
            }
            for main_heading, subheadings in SectionContent.SUBHEADING_GROUPS
        ]
        return super().changelist_view(request, extra_context=extra_context)
