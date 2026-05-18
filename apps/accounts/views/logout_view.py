from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        response = Response({"message": "Logout ok"}, status=200)
        response.delete_cookie(key="refresh_token", path="/api/auth/", samesite="None")

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception:
                pass  # cookie já será apagado de qualquer forma
        return response
