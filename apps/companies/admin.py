from django.contrib import admin

from apps.companies.models import Company
from apps.professionals.models import Professional
from apps.services.models import Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1


class ProfessionalInline(admin.TabularInline):
    model = Professional
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "city", "state", "rating", "active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "cnpj", "email")
    list_filter = ("category", "state", "active")

    inlines = [ServiceInline, ProfessionalInline]
