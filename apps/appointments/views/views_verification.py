from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.appointments.serializers.verification_serializer import AppointmentVerificationRequestSerializer
from apps.appointments.services.verify_appointment_service import verify_appointment_by_token


class PublicVerifyAppointmentView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=AppointmentVerificationRequestSerializer)
    def post(self, request):
        serializer = AppointmentVerificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment = verify_appointment_by_token(token=serializer.validated_data["token"])

        return Response(
            {
                "id": str(appointment.id),
                "status": appointment.status,
                "date": appointment.date,
                "time": appointment.time.strftime("%H:%M"),
            }
        )
