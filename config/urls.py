from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.appointments.views.views_public import PublicAvailabilityView, PublicCreateBookingView
from apps.companies.views.public_company_view import PublicCompanyView
from apps.professionals.views.views_public import PublicCompanyServiceProfessionalsView
from apps.services.views.views_public import PublicCompanyServicesView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/subscriptions/", include("apps.subscriptions.urls")),
    # suas rotas já existentes...
    path("api/auth/", include("apps.accounts.urls")),
    # rotas públicas de agendamento (compatíveis com o frontend atual)
    path("api/public/company/<slug:slug>/", PublicCompanyView.as_view()),
    path("api/public/company/<slug:slug>/services/", PublicCompanyServicesView.as_view()),
    path(
        "api/public/company/<slug:slug>/services/<uuid:service_uid>/professionals/",
        PublicCompanyServiceProfessionalsView.as_view(),
    ),
    path("api/public/company/<slug:slug>/availability/", PublicAvailabilityView.as_view()),
    path("api/public/bookings/", PublicCreateBookingView.as_view()),
]
