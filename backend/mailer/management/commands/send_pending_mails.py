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
            # attempts stored in context JSON
            ctx = m.context or {}
            attempts = int(ctx.get("attempts", 0))
            if attempts >= 5:
                self.stdout.write(f"Skipping {m.email} (max attempts)")
                continue

            # try to render template if template looks like a template path
            html_body = ""
            try:
                if m.template:
                    html_body = render_to_string(m.template, ctx)
                else:
                    html_body = ctx.get("html", "")
            except Exception:
                html_body = ctx.get("html", "")

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