from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Diagnostica a configuração de e-mail e, opcionalmente, envia um e-mail de teste."

    def add_arguments(self, parser):
        parser.add_argument(
            "--send",
            action="store_true",
            help="Envia o e-mail de teste em vez de apenas mostrar as configurações.",
        )
        parser.add_argument(
            "--to",
            type=str,
            default=None,
            help="Destinatário do e-mail de teste. Obrigatório quando usado com --send.",
        )
        parser.add_argument(
            "--subject",
            type=str,
            default="Teste de e-mail",
            help="Assunto do e-mail de teste.",
        )
        parser.add_argument(
            "--message",
            type=str,
            default="Este é um e-mail de teste enviado pelo Django.",
            help="Conteúdo do e-mail de teste.",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("== Configuração atual de e-mail =="))
        self.stdout.write(f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', '')}")
        self.stdout.write(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', '')}")
        self.stdout.write(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', '')}")
        self.stdout.write(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', '')}")
        self.stdout.write(
            f"EMAIL_HOST_PASSWORD_SET: {bool(getattr(settings, 'EMAIL_HOST_PASSWORD', ''))}"
        )
        self.stdout.write(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', '')}")
        self.stdout.write(f"EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', '')}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', '')}")

        if not options["send"]:
            self.stdout.write(
                self.style.WARNING(
                    "\nUse --send para enviar um e-mail de teste.\n"
                    "Exemplo:\n"
                    "python manage.py send_test_email --send --to seu-email@exemplo.com"
                )
            )
            return

        recipient = options.get("to")
        if not recipient:
            raise CommandError("Você precisa informar --to quando usar --send.")

        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
            settings, "EMAIL_HOST_USER", None
        )
        if not from_email:
            raise CommandError(
                "DEFAULT_FROM_EMAIL ou EMAIL_HOST_USER precisa estar configurado."
            )

        connection = get_connection(
            backend=getattr(settings, "EMAIL_BACKEND", None),
            fail_silently=False,
        )

        email = EmailMessage(
            subject=options["subject"],
            body=options["message"],
            from_email=from_email,
            to=[recipient],
            connection=connection,
        )

        sent_count = email.send(fail_silently=False)

        if sent_count:
            self.stdout.write(
                self.style.SUCCESS(f"E-mail enviado com sucesso para {recipient}")
            )
        else:
            self.stdout.write(
                self.style.ERROR("O Django não retornou confirmação de envio.")
            )
