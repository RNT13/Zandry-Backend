from django.urls import path

from apps.services.views.views_public import PublicCompanyServicesView

urlpatterns = [
    path("public/company/<slug:slug>/services/", PublicCompanyServicesView.as_view(), name="public-company-services"),
]
