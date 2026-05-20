from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.companies.models import Company
from apps.professionals.serializers.public_response_serializer import PublicProfessionalBriefSerializer
from apps.services.models import Service


class PublicCompanyServiceProfessionalsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses={200: PublicProfessionalBriefSerializer(many=True)})
    def get(self, request, slug, service_uid):
        company = get_object_or_404(Company, slug=slug, active=True)
        service = get_object_or_404(Service, id=service_uid, company=company, active=True)

        professionals = service.professionals.filter(active=True).order_by("full_name")

        serializer = PublicProfessionalBriefSerializer(professionals, many=True, context={"request": request})
        return Response(serializer.data)
