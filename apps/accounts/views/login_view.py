from django.conf import settings
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers.auth_request_serializer import LoginRequestSerializer
from apps.accounts.serializers.auth_response_serializer import LoginResponseSerializer


def get_user_company_slug(user):
    company = getattr(user, "company", None)
    return company.slug if company else None


def set_auth_cookies(response, refresh_token, company_slug=None, remember_me=False):
    refresh_max_age = 30 * 24 * 60 * 60 if remember_me else 24 * 60 * 60

    cookie_kwargs = {
        "httponly": True,
        "secure": not settings.DEBUG,
        "samesite": "None" if not settings.DEBUG else "Lax",
        "path": "/",
    }

    response.set_cookie(
        key="refresh_token",
        value=str(refresh_token),
        max_age=refresh_max_age,
        **cookie_kwargs,
    )

    if company_slug:
        response.set_cookie(
            key="company_slug",
            value=company_slug,
            max_age=refresh_max_age,
            **cookie_kwargs,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginRequestSerializer, responses={200: LoginResponseSerializer})
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        remember_me = serializer.validated_data.get("remember_me", False)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response(
                {"success": False, "message": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"success": False, "message": "Usuário inativo."},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)
        company_slug = get_user_company_slug(user)

        response_data = {
            "success": True,
            "message": "Login realizado com sucesso.",
            "access": str(refresh.access_token),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "company_slug": company_slug,
            },
        }

        response = Response(response_data, status=status.HTTP_200_OK)
        set_auth_cookies(
            response=response,
            refresh_token=refresh,
            company_slug=company_slug,
            remember_me=remember_me,
        )
        return response
