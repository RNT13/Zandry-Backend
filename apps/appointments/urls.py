from django.urls import path

from apps.appointments.views.views_public import PublicAvailabilityView, PublicCreateBookingView
from apps.appointments.views.views_verification import PublicVerifyAppointmentView

urlpatterns = [
    path("public/company/<slug:slug>/availability/", PublicAvailabilityView.as_view(), name="public-availability"),
    path("public/bookings/", PublicCreateBookingView.as_view(), name="public-booking-create"),
    path("public/bookings/verify/", PublicVerifyAppointmentView.as_view(), name="public-booking-verify"),
]
