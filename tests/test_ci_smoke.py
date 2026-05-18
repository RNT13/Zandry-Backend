from django.urls import reverse
from rest_framework.test import APIClient


def test_dashboard_requires_authentication():
    client = APIClient()
    url = reverse("dashboard-summary")
    response = client.get(url)
    assert response.status_code == 401
