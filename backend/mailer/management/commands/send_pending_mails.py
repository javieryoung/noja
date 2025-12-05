from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from mailer.models import Mailer
from mailer.ses import send_email_ses

class Command(BaseCommand):
    help = "Envía Mailer pendientes (sent_on is null) usando SES"

    def handle(self, *args, **options):
        batch_size = 100
        qs = Mailer.objects.filter(sent_on__isnull=True).order_by("id")[:batch_size]

        for m in qs:
            ctx = m.context or {}
            attempts = int(ctx.get("attempts", 0))
            if attempts >= 5:
                self.stdout.write(f"Skipping {m.email} (max attempts)")
                continue

            # Render del template o usar HTML guardado
            html_body = ""
            try:
                if m.template:
                    # ⚠️ Usamos el HTML ya guardado en el contexto
                    html_body = ctx.get("html", "")
                else:
                    html_body = ctx.get("html", "")
            except Exception as e:
                self.stdout.write(f"Error renderizando template: {e}")
                html_body = ctx.get("html", "")

            # Envío real por SES
            res = send_email_ses(m.email, m.subject, html_body)

            if res.get("status") == "ok":
                m.sent_on = timezone.now()
                ctx["message_id"] = res.get("message_id")
                ctx["last_error"] = ""
            else:
                attempts += 1
                ctx["attempts"] = attempts
                ctx["last_error"] = res.get("details", "")
            m.context = ctx
            m.save()

            self.stdout.write(f"{m.email} -> {res.get('status')}")
