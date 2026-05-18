from django.urls import path

from apps.clients.views.client_views import ClientListView

urlpatterns = [
    path("", ClientListView.as_view(), name="client-list"),
]
