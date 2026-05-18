from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.companies.models import Company
from apps.services.models import Service
from apps.professionals.models import Professional
from apps.appointments.serializers.public_request_serializer import (
    PublicAvailabilityQuerySerializer,
    PublicCreateBookingSerializer,
)
from apps.appointments.serializers.public_response_serializer import (
    PublicAvailabilityResponseSerializer,
    PublicBookingResponseSerializer,
)
from apps.appointments.services.public_availability_service import build_public_availability
from apps.appointments.services.public_booking_service import create_public_booking


class PublicAvailabilityView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[PublicAvailabilityQuerySerializer],
        responses={200: PublicAvailabilityResponseSerializer}
    )
    def get(self, request, slug):
        company = get_object_or_404(Company, slug=slug, active=True)

        query_serializer = PublicAvailabilityQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        params = query_serializer.validated_data

        service = get_object_or_404(Service, id=params["service_uid"], company=company, active=True)
        professional = get_object_or_404(
            Professional,
            id=params["professional_uid"],
            company=company,
            active=True,
            services=service,
        )

        data = build_public_availability(
            company=company,
            professional=professional,
            service=service,
            start_day=params.get("date"),
        )

        return Response(data, status=status.HTTP_200_OK)


class PublicCreateBookingView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PublicCreateBookingSerializer,
        responses={201: PublicBookingResponseSerializer}
    )
    def post(self, request):
        serializer = PublicCreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = create_public_booking(serializer.validated_data)

        return Response(
            {
                "success": True,
                "message": "Agendamento criado com sucesso.",
                "booking": booking,
            },
            status=status.HTTP_201_CREATED,
        )
