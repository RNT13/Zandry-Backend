from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.serializers.auth_response_serializer import RefreshResponseSerializer


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


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    @extend_schema(request=None, responses={200: RefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")
        if not refresh:
            return Response({"detail": "Refresh ausente."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data={"refresh": refresh})
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.validated_data)
        new_refresh = data.pop("refresh", None)

        response = Response(data, status=status.HTTP_200_OK)

        if new_refresh:
            set_refresh_cookie(
                response,
                new_refresh,
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
            )

        return response
