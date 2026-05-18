from django.db import transaction
from apps.clients.models import Client


@transaction.atomic
def upsert_public_client(company, validated_data: dict) -> Client:
    full_name = validated_data["full_name"].strip()
    phone = validated_data["phone"].strip()
    email = validated_data.get("email") or None

    client, created = Client.objects.update_or_create(
        company=company,
        phone=phone,
        defaults={
            "full_name": full_name,
            "email": email,
        },
    )

    return client
