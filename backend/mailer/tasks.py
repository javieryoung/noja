# mailer/tasks.py
import json
from django.template.loader import render_to_string
from django.utils.timezone import now
from mailer.models import Mailer
from mailer.ses import send_email_ses

def _normalize_context(raw):
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    # si viene como string JSON
    return json.loads(raw)

def send_pending_mails_via_ses(client=None):
    enviados = 0
    for mail in Mailer.objects.filter(sent_on__isnull=True):
        context = _normalize_context(mail.context)
        context["subject"] = mail.subject
        html_body = render_to_string(mail.template, context)
        result = send_email_ses(
            to_email=mail.email,
            subject=mail.subject,
            html_body=html_body,
            client=client   # ← usa el stub
        )
        if result.get("status") == "ok":
            mail.sent_on = now()
            mail.save(update_fields=["sent_on"])
            enviados += 1
    return enviados