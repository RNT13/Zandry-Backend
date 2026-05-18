from django.contrib import admin

from apps.services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "price", "duration", "active")
    search_fields = ("name",)
    list_filter = ("company",)
