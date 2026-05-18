from django.urls import path

from apps.subscriptions.views.subscription_views import SubscriptionPlanListView

urlpatterns = [
    path("plans/", SubscriptionPlanListView.as_view(), name="subscription-plan-list"),
]
