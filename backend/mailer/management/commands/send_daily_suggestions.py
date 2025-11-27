# mailer/management/commands/send_daily_suggestions.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from home.models import Suggestion
from mailer.models import Mailer
from mailer.utils import render_remote_template
from mailer.ses import send_email_ses

class Command(BaseCommand):
    help = "Envía el correo con las sugerencias del día"

    def handle(self, *args, **options):
        hoy = timezone.now().date()
        sugerencias = Suggestion.objects.filter(date__date=hoy)

        if not sugerencias.exists():
            self.stdout.write("No hay sugerencias para hoy.")
            return

        contexto = {
            "suggestions": [
                {
                    "symbol": s.symbol,
                    "title": s.title,
                    "description": s.description,
                    "direction": s.get_direction_display(),
                    "date": s.date,
                    "new_url": s.new.get_absolute_url(),
                }
                for s in sugerencias
            ]
        }

        # Renderizamos el template remoto (emails/suggestions.html)
        html = render_remote_template("templates/mailer/suggestions.html", contexto)

        # Creamos un registro en Mailer (opcional, para trazabilidad)
        mail = Mailer.objects.create(
            email="destinatario@dominio.com",  # o lista de destinatarios
            subject="Sugerencias del día",
            template="emails/suggestions.html",
            context=contexto,
        )

        try:
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