import json
from django.template.loader import render_to_string
from django.utils.timezone import now
from home.models import Suggestion
from mailer.models import Mailer
from mailer.ses import send_email_ses


def send_daily_suggestions_via_ses():
    hoy = now().date()
    sugerencias = Suggestion.objects.filter(date__date=hoy)
    
    if not sugerencias.exists():
        return 0
    

    contexto_template = {
        "suggestions": [{"symbol": s.symbol, ...} for s in sugerencias]
    }
    html = render_to_string("mailer/suggestions.html", contexto_template)
    
    creados = 0
    for destinatario in Mailer.objects.filter(active=True):  # Filtrar activos
        Mailer.objects.create(
            email=destinatario.email,
            subject="Sugerencias del día",
            body=html,  # Guardar HTML directamente
            template=None,  # No re-renderizar
            context={"html": html},  # Para compatibilidad
        )
        creados += 1
    return creados



def send_pending_mails_via_ses():
    pendientes = Mailer.objects.filter(sent_on__isnull=True)

    enviados = 0
    for mail in pendientes:
        contexto = mail.context
        if isinstance(contexto, str):
            try:
                contexto = json.loads(contexto)
            except json.JSONDecodeError:
                contexto = {}

        html = render_to_string(mail.template, contexto)

        resultado = send_email_ses(
            to_email=mail.email,
            subject=mail.subject,
            html_body=html,
        )

        if resultado["status"] == "ok":
            mail.sent_on = now()
            mail.save()
            enviados += 1

    return enviados