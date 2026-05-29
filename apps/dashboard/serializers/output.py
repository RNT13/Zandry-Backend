from rest_framework import serializers


class DashboardSummaryQuerySerializer(serializers.Serializer):
    days = serializers.IntegerField(min_value=1, max_value=90, default=7)


class DashboardTotalsSerializer(serializers.Serializer):
    clients = serializers.IntegerField()
    professionals = serializers.IntegerField()
    services = serializers.IntegerField()
    appointments = serializers.IntegerField()


class DashboardAppointmentsSerializer(serializers.Serializer):
    today = serializers.IntegerField()
    tomorrow = serializers.IntegerField()
    pending = serializers.IntegerField()
    confirmed = serializers.IntegerField()
    completed = serializers.IntegerField()
    cancelled = serializers.IntegerField()


class DashboardRevenueSerializer(serializers.Serializer):
    completed_count = serializers.IntegerField()
    completed_amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class DashboardDailyPointSerializer(serializers.Serializer):
    date = serializers.DateField()
    total = serializers.IntegerField()


class DashboardSummarySerializer(serializers.Serializer):
    period_days = serializers.IntegerField()
    totals = DashboardTotalsSerializer()
    appointments = DashboardAppointmentsSerializer()
    revenue = DashboardRevenueSerializer()
    recent_daily = DashboardDailyPointSerializer(many=True)
