from django.contrib import admin
from apps.professionals.models import Professional


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company", "position", "rating", "active")
    search_fields = ("full_name",)
    list_filter = ("company", "position")
    filter_horizontal = ("services",)
