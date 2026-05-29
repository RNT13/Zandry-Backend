from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.auth_response_serializer import RegisterCompanyResponseSerializer
from apps.accounts.serializers.register_company_serializer import RegisterCompanySerializer
from apps.accounts.services import register_company_service


def set_refresh_cookie(response, refresh_token, max_age=None):
    response.set_cookie(
        key="refresh_token",
        value=str(refresh_token),
        max_age=max_age,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="None" if not settings.DEBUG else "Lax",
        path="/",
    )


class RegisterCompanyView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterCompanySerializer, responses={201: RegisterCompanyResponseSerializer})
    def post(self, request):
        serializer = RegisterCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = register_company_service(serializer.validated_data)

            refresh_token = result.pop("refresh", None)

            response = Response(result, status=status.HTTP_201_CREATED)

            if refresh_token:
                set_refresh_cookie(
                    response,
                    refresh_token,
                    max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
                )

            return response

        except ValidationError as exc:
            return Response(
                {
                    "success": False,
                    "message": exc.detail if isinstance(exc.detail, str) else "Erro de validação.",
                    "errors": exc.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as exc:
            return Response(
                {
                    "success": False,
                    "message": "Erro interno ao cadastrar a empresa.",
                    "detail": str(exc) if settings.DEBUG else None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
