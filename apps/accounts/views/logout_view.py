from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=None, responses={200: None})
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        response = Response({"message": "Logout ok"}, status=status.HTTP_200_OK)

        response.delete_cookie(
            key="refresh_token",
            path="/",
            samesite="None" if not settings.DEBUG else "Lax",
        )

        response.delete_cookie(
            key="company_slug",
            path="/",
            samesite="None" if not settings.DEBUG else "Lax",
        )

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception:
                pass

        return response
