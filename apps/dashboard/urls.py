from django.urls import path

from apps.dashboard.views.dashboard_views import DashboardSummaryView

urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
]
