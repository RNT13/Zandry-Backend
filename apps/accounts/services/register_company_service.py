from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

from apps.accounts.models import User
from apps.companies.models import Company
from apps.subscriptions.models import SubscriptionPlan, SubscriptionUsage
from apps.services.models import Service
from apps.professionals.models import Professional
from apps.companies.models.business_hours_model import BusinessHour


def generate_unique_slug(company_name: str) -> str:
    """
    Gera um slug único baseado no nome da empresa.
    Exemplo:
        "Salão Bella" -> "salao-bella"
        Se já existir -> "salao-bella-2"
    """
    base_slug = slugify(company_name)
    slug = base_slug
    counter = 2

    while Company.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


@transaction.atomic
def register_company_service(validated_data: dict) -> dict:
    """
    Recebe o payload validado do RegisterCompanySerializer e cria:
    - Owner User
    - Company
    - SubscriptionUsage
    - Services
    - Professionals + vínculos com services
    - Tokens JWT (login automático)
    """

    # ------------------------------------------------------------------
    # Separação dos blocos do payload
    # ------------------------------------------------------------------
    owner_data = validated_data["owner"]
    company_data = validated_data["company"]
    address_data = validated_data["address"]
    business_hours_data = validated_data.get("business_hours", [])
    advantages_data = validated_data["advantages"]
    services_data = validated_data.get("services", [])
    professionals_data = validated_data.get("professionals", [])
    subscription_data = validated_data["subscription"]

    # ------------------------------------------------------------------
    # Dados básicos
    # ------------------------------------------------------------------
    company_name = company_data["company_name"]
    company_email = company_data["email"]
    company_phone = company_data["phone"]

    # ------------------------------------------------------------------
    # Validações de unicidade
    # ------------------------------------------------------------------
    if Company.objects.filter(cnpj=company_data["cnpj"]).exists():
        raise ValidationError({"company": {"cnpj": "Já existe uma empresa com este CNPJ."}})

    if Company.objects.filter(email=company_email).exists():
        raise ValidationError("Já existe uma empresa cadastrada com este e-mail.")

    if User.objects.filter(email=owner_data["email"]).exists():
        raise ValidationError("Já existe um usuário cadastrado com este e-mail.")

    # ------------------------------------------------------------------
    # Busca do plano
    # ------------------------------------------------------------------
    selected_plan = subscription_data["selected_plan"]

    try:
        plan = SubscriptionPlan.objects.get(code=selected_plan)
    except SubscriptionPlan.DoesNotExist:
        raise ValidationError({"subscription": {"selected_plan": "Plano inválido."}})

    # ------------------------------------------------------------------
    # Criação da Company
    # ------------------------------------------------------------------
    company = Company.objects.create(
        name=company_name,
        slug=generate_unique_slug(company_name),
        cnpj=company_data["cnpj"],
        email=company_email,
        phone=company_data["phone"],
        category=company_data["category"],
        description=company_data["description"],
        cep=address_data["cep"],
        address=address_data["address"],
        number=address_data["number"],
        city=address_data["city"],
        state=address_data["state"],
        advantage1=advantages_data.get("advantage1", ""),
        advantage2=advantages_data.get("advantage2", ""),
        advantage3=advantages_data.get("advantage3", ""),
    )

    # ------------------------------------------------------------------
    # Criação do Owner User
    # ------------------------------------------------------------------
    owner = User.objects.create_user(
        company=company,
        full_name=owner_data["full_name"],
        email=owner_data["email"],
        phone=owner_data.get("phone", ""),
        password=owner_data["password"],
        role="owner",
    )

    # ------------------------------------------------------------------
    # Criação da assinatura/uso
    # ------------------------------------------------------------------
    expires_at = timezone.now() + timedelta(days=plan.trial_days or 30)

    status = "trial" if selected_plan == "trial" else "active"

    SubscriptionUsage.objects.create(
        company=company,
        plan=plan,
        status=status,
        expires_at=expires_at,
    )

    # ------------------------------------------------------------------
    # Criação dos BusinessHours
    # ------------------------------------------------------------------
    for item in business_hours_data:
        BusinessHour.objects.create(
            company=company,
            week_day=item["week_day"],
            start=item.get("start", ""),
            end=item.get("end", ""),
            is_open=item.get("is_open", False),
        )

    # ------------------------------------------------------------------
    # Criação dos Services
    # ------------------------------------------------------------------
    created_services_map = {}

    for index, service_data in enumerate(services_data):
        service = Service.objects.create(
            company=company,
            name=service_data["name"],
            description=service_data.get("description", ""),
            price=service_data["price"],
            duration=service_data["duration"],
        )

        # Mapeia o ID temporário do frontend para o UUID real do banco
        temp_id = service_data.get("uid") or service_data.get("id") or str(index)
        created_services_map[str(temp_id)] = service

    # ------------------------------------------------------------------
    # Criação dos Professionals e vínculos ManyToMany
    # ------------------------------------------------------------------
    for professional_data in professionals_data:
        professional = Professional.objects.create(
            company=company,
            full_name=professional_data["full_name"],
            position=professional_data["position"],
            phone=professional_data.get("phone", ""),
        )

        linked_services = []

        for service_temp_id in professional_data.get("services_ids", []):
            service = created_services_map.get(str(service_temp_id))
            if service:
                linked_services.append(service)

        professional.services.set(linked_services)

    # ------------------------------------------------------------------
    # Geração de JWT (login automático)
    # ------------------------------------------------------------------
    refresh = RefreshToken.for_user(owner)

    # ------------------------------------------------------------------
    # Resposta final
    # ------------------------------------------------------------------
    return {
        "message": "Empresa cadastrada com sucesso.",
        "success": True,
        "user": {
            "id": str(owner.id),
            "full_name": owner.full_name,
            "phone": owner.phone,
            "email": owner.email,
            "created_at": owner.created_at.isoformat(),
        },
        "company_id": str(company.id),
        "company_slug": company.slug,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
