from django.urls import path

from apps.appointments.views.views_public import PublicAvailabilityView, PublicCreateBookingView

urlpatterns = [
    path("public/company/<slug:slug>/availability/", PublicAvailabilityView.as_view(), name="public-availability"),
    path("public/bookings/", PublicCreateBookingView.as_view(), name="public-booking-create"),
]
