from django.urls import path
from apps.notifications.views.views_in_app import MyNotificationListView, MarkNotificationAsReadView
from apps.notifications.views.views_dashboard import MyNotificationPreferenceView

urlpatterns = [
    path("inbox/", MyNotificationListView.as_view(), name="notification-inbox"),
    path("read/", MarkNotificationAsReadView.as_view(), name="notification-mark-read"),
    path("preferences/", MyNotificationPreferenceView.as_view(), name="notification-preferences"),
]
