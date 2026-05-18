from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.companies.models import Company
from apps.companies.serializers.company_read_serializer import CompanyReadSerializer


class PublicCompanyView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses={200: CompanyReadSerializer, 404: OpenApiResponse(description="Company not found")})
    def get(self, request, slug):
        company = get_object_or_404(Company, slug=slug, active=True)
        serializer = CompanyReadSerializer(company, context={"request": request})
        return Response(serializer.data)
