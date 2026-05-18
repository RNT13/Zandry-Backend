from django.core.management.base import BaseCommand
from apps.subscriptions.models.plan_model import SubscriptionPlan
from decimal import Decimal

PLANS_SEED = [
    {
        "code":        "trial",
        "name":        "Trial",
        "title":       "Teste grátis",
        "subtitle":    "Teste todas as funcionalidades",
        "description": "Conheça a plataforma sem precisar de cartão.",
        "recommended": False,
        "coming_soon": False,
        "monthly_price": Decimal(0),
        "max_professionals": 1,
        "max_services":     3,
        "max_appointments": 30,
        "allow_chat":           False,
        "allow_reports":        False,
        "allow_automation":     False,
        "allow_full_dashboard": False,
        "trial_days": 15,
        "features": [
            "Acesso completo por 15 dias",
            "Todas as funcionalidades liberadas",
            "Sem cartão de crédito",
        ],
        "sort_order": 1,
        "is_active":  True,
    },
    {
        "code":        "start",
        "name":        "Start",
        "title":       "Plano Start",
        "subtitle":    "Ideal para pequenos negócios",
        "description": "Para quem está começando a organizar seus agendamentos.",
        "recommended": False,
        "coming_soon": False,
        "monthly_price": Decimal(49.90),
        "max_professionals": 5,
        "max_services":     10,
        "max_appointments": 200,
        "allow_chat":           False,
        "allow_reports":        False,
        "allow_automation":     False,
        "allow_full_dashboard": False,
        "trial_days": 0,
        "features": [
            "Até 5 profissionais",
            "Até 10 serviços",
            "Até 200 agendamentos/mês",
            "Dashboard gerencial básico",
        ],
        "sort_order": 2,
        "is_active":  True,
    },
    {
        "code":        "pro",
        "name":        "Pro",
        "title":       "Plano Pro",
        "subtitle":    "Mais escolhido",
        "description": "Completo para negócios em crescimento.",
        "recommended": True,
        "coming_soon": False,
        "monthly_price": Decimal(99.90),
        "max_professionals": 15,
        "max_services":     40,
        "max_appointments": 1000,
        "allow_chat":           False,
        "allow_reports":        True,
        "allow_automation":     True,
        "allow_full_dashboard": True,
        "trial_days": 0,
        "features": [
            "Tudo do Start +",
            "Até 15 profissionais",
            "Até 40 serviços",
            "Até 1.000 agendamentos/mês",
            "Relatórios de desempenho",
            "Dashboard avançado",
        ],
        "sort_order": 3,
        "is_active":  True,
    },
    {
        "code":        "business",
        "name":        "Business",
        "title":       "Plano Business",
        "subtitle":    "Estrutura corporativa",
        "description": "Para operações robustas e escaláveis.",
        "recommended": False,
        "coming_soon": True,
        "monthly_price": Decimal(199.90),
        "max_professionals": 999,
        "max_services":     999,
        "max_appointments": 99999,
        "allow_chat":           True,
        "allow_reports":        True,
        "allow_automation":     True,
        "allow_full_dashboard": True,
        "trial_days": 0,
        "features": [
            "Tudo do Pro +",
            "Profissionais ilimitados",
            "Múltiplas unidades",
            "Chat interno",
            "Dashboard corporativo",
        ],
        "sort_order": 4,
        "is_active":  True,
    },
]


class Command(BaseCommand):
    help = "Atualiza os planos de assinatura com os dados da seed"

    def handle(self, *args, **kwargs):
        for item in PLANS_SEED:
            data = item.copy()
            code = data.pop("code")
            obj, created = SubscriptionPlan.objects.update_or_create(
                code=code, defaults=data
            )
            action = "criado" if created else "atualizado"
            self.stdout.write(f"{code} → {action}")
        self.stdout.write(self.style.SUCCESS("Seed concluída."))
