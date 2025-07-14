from django.contrib import admin
from .models import Profile, Skill, Project, Experience, ContactSubmission, PageVisit

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'bio')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('-proficiency',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'technologies')
    search_fields = ('title', 'description')
    filter_horizontal = ('technologies',)
    ordering = ('-created_at',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'company', 'start_date', 'end_date')
    search_fields = ('position', 'company', 'description')
    filter_horizontal = ('technologies',)
    ordering = ('-start_date',)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected submissions as read"

    actions = ['mark_as_read']

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('page', 'ip_address', 'timestamp')
    list_filter = ('page', 'timestamp')
    search_fields = ('page', 'ip_address')
    ordering = ('-timestamp',)
