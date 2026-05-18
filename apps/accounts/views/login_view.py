from datetime import timedelta

from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers.auth_request_serializer import LoginRequestSerializer
from apps.accounts.serializers.auth_response_serializer import LoginResponseSerializer


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

        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))
        else:
            refresh.set_exp(lifetime=timedelta(days=1))

        response_data = {
            "success": True,
            "message": "Login realizado com sucesso.",
            "access": str(refresh.access_token),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "company_slug": user.company.slug if user.company else None,
            },
        }

        response = Response(response_data, status=200)

        max_age = 30 * 24 * 60 * 60 if remember_me else 24 * 60 * 60
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            max_age=max_age,
            httponly=True,
            secure=True,
            samesite="None",
            path="/api/auth/",
        )

        return response
