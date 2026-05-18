from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.companies.models import Company
from apps.services.models import Service
from apps.services.serializers.public_response_serializer import PublicServiceSerializer


class PublicCompanyServicesView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses={200: PublicServiceSerializer(many=True)})
    def get(self, request, slug):
        company = get_object_or_404(Company, slug=slug, active=True)
        services = (
            Service.objects
            .filter(company=company, active=True)
            .prefetch_related("professionals")
            .order_by("name")
        )
        serializer = PublicServiceSerializer(services, many=True, context={"request": request})
        return Response(serializer.data)
