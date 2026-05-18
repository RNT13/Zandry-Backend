from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.companies.models import Company
from apps.companies.serializers.public_availability_serializer import PublicAvailabilitySerializer
from apps.companies.services.public_availability_service import build_public_availability
from apps.professionals.models import Professional
from apps.services.models import Service


class PublicCompanyAvailabilityView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: PublicAvailabilitySerializer,
            404: OpenApiResponse(description="Company, service or professional not found"),
        }
    )
    def get(self, request, slug):
        company = get_object_or_404(Company, slug=slug, active=True)

        service_uid = request.query_params.get("service_uid")
        professional_uid = request.query_params.get("professional_uid")
        date = request.query_params.get("date")

        if not service_uid or not professional_uid:
            return Response(
                {"detail": "service_uid e professional_uid são obrigatórios."},
                status=400,
            )

        service = get_object_or_404(Service, uid=service_uid, company=company)
        professional = get_object_or_404(Professional, uid=professional_uid, company=company)

        payload = build_public_availability(
            company=company,
            service=service,
            professional=professional,
            date=date,
        )

        serializer = PublicAvailabilitySerializer(payload)
        return Response(serializer.data)
