from django.urls import path

from apps.professionals.views.views_public import PublicCompanyServiceProfessionalsView

urlpatterns = [
    path(
        "public/company/<slug:slug>/services/<uuid:service_uid>/professionals/",
        PublicCompanyServiceProfessionalsView.as_view(),
        name="public-company-service-professionals",
    ),
]
