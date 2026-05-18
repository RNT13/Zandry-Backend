from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/subscriptions/", include("apps.subscriptions.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/clients/", include("apps.clients.urls")),
    path("api/", include("apps.companies.urls")),
    path("api/", include("apps.services.urls")),
    path("api/", include("apps.professionals.urls")),
    path("api/", include("apps.appointments.urls")),
]
