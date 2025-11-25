# mailer/management/commands/send_pending_mails.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from mailer.models import Mailer
from mailer.utils import render_remote_template
from mailer.ses import send_email_ses

class Command(BaseCommand):
    help = "Envía los correos pendientes registrados en el modelo Mailer"

    def handle(self, *args, **options):
        pendientes = Mailer.objects.filter(sent_on__isnull=True)
        self.stdout.write(f"Encontrados {pendientes.count()} correos pendientes.")

        for mail in pendientes:
            try:
                # Renderizar template remoto con contexto
                html = render_remote_template(mail.template, mail.context)

                # Enviar correo vía SES
                resultado = send_email_ses(
                    to_email=mail.email,
                    subject=mail.subject,
                    html_body=html
                )

                if resultado["status"] == "ok":
                    mail.sent_on = timezone.now()
                    mail.save()
                    self.stdout.write(self.style.SUCCESS(f"Enviado a {mail.email}"))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Error con {mail.email}: {resultado['details']}"
                    ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Falló {mail.email}: {str(e)}"
                ))
