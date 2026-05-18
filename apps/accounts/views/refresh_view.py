from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.serializers.auth_response_serializer import RefreshResponseSerializer


class CookieTokenRefreshView(TokenRefreshView):
    @extend_schema(request=None, responses={200: RefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")
        if not refresh:
            return Response({"detail": "Refresh ausente."}, status=401)

        data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)
        data["refresh"] = refresh
        request._full_data = data

        response = super().post(request, *args, **kwargs)

        new_refresh = response.data.pop("refresh", None)
        if new_refresh:
            response.set_cookie(
                key="refresh_token",
                value=new_refresh,
                max_age=30 * 24 * 60 * 60,
                httponly=True,
                secure=True,
                samesite="None",
                path="/api/auth/",
            )

        return response
