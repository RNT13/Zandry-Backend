from rest_framework import serializers


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


class DashboardSummarySerializer(serializers.Serializer):
    totals = DashboardTotalsSerializer()
    appointments = DashboardAppointmentsSerializer()
    revenue = DashboardRevenueSerializer()
