from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dashboard.permissions import IsCompanyUser
from apps.dashboard.selectors.dashboard_queries import get_dashboard_summary
from apps.dashboard.serializers.output import DashboardSummarySerializer


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyUser]

    @extend_schema(responses={200: DashboardSummarySerializer})
    def get(self, request):
        payload = get_dashboard_summary(company=request.user.company)
        return Response(payload)
