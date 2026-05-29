from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dashboard.permissions import IsCompanyUser
from apps.dashboard.selectors.dashboard_queries import get_dashboard_summary
from apps.dashboard.serializers.output import (
    DashboardSummaryQuerySerializer,
    DashboardSummarySerializer,
)


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
        query_serializer = DashboardSummaryQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        payload = get_dashboard_summary(
            company=request.user.company,
            period_days=query_serializer.validated_data["days"],
        )

        return Response(payload)
