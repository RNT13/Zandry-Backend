from django.urls import path

from apps.companies.views.public_company_availability_view import PublicCompanyAvailabilityView
from apps.companies.views.public_company_view import PublicCompanyView

urlpatterns = [
    path("public/company/<slug:slug>/", PublicCompanyView.as_view(), name="public-company-detail"),
    path(
        "public/company/<slug:slug>/availability/",
        PublicCompanyAvailabilityView.as_view(),
        name="public-company-availability",
    ),
]
