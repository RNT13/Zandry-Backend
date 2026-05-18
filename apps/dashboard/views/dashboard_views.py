from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dashboard.permissions import IsCompanyUser
from apps.dashboard.selectors.dashboard_queries import get_dashboard_summary
from apps.dashboard.serializers.output import DashboardSummarySerializer


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyUser]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="days",
                type=int,
                required=False,
                description="Período em dias para a série diária (1 a 90). Padrão: 7.",
            )
        ],
        responses={200: DashboardSummarySerializer},
    )
    def get(self, request):
        days = request.query_params.get("days", 7)
        payload = get_dashboard_summary(company=request.user.company, period_days=days)
        return Response(payload)
