from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.accounts.serializers.register_company_serializer import RegisterCompanySerializer
from apps.accounts.serializers.auth_response_serializer import RegisterCompanyResponseSerializer
from apps.accounts.services import register_company_service


class RegisterCompanyView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterCompanySerializer,
        responses={201: RegisterCompanyResponseSerializer}
    )
    def post(self, request):
        serializer = RegisterCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = register_company_service(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as exc:
            return Response(
                {
                    "success": False,
                    "message": "Erro interno ao cadastrar a empresa.",
                    "detail": str(exc) if settings.DEBUG else None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
