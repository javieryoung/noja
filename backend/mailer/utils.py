import json
from django.template.loader import render_to_string
from django.utils.timezone import now
from home.models import Suggestion
from mailer.models import Mailer
from mailer.ses import send_email_ses


def render_local_template(template_name, context):
    """
    Renderiza un template local de Django y devuelve el HTML como string.
    """
    return render_to_string(template_name, context)


def send_daily_suggestions_via_ses():
    """
    Envía las sugerencias del día a todos los destinatarios del modelo Mailer
    usando el template local 'mailer/suggestions.html'.

    hoy = now().date()

    sugerencias = Suggestion.objects.filter(date__date=hoy)
    """
    sugerencias = Suggestion.objects.all()  # solo para probar, sin filtro de fecha

    if not sugerencias.exists():
        return 0  # nada para enviar

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

    html = render_local_template("mailer/suggestions.html", contexto)

    enviados = 0
    mailer_objs = Mailer.objects.all()

    for mail in mailer_objs:
        resultado = send_email_ses(
            to_email=mail.email,
            subject="Sugerencias del día",
            html_body=html,
        )
        if resultado["status"] == "ok":
            mail.sent_on = now()
            mail.save()
            enviados += 1

    return enviados


def send_pending_mails_via_ses():
    """
    Envía los correos pendientes del modelo Mailer,
    renderizando el template local indicado en Mailer.template
    con el contexto de Mailer.context.
    """
    pendientes = Mailer.objects.filter(sent_on__isnull=True)

    enviados = 0
    for mail in pendientes:
        # mail.context puede ser dict (JSONField) o string JSON
        contexto = mail.context
        if isinstance(contexto, str):
            try:
                contexto = json.loads(contexto)
            except json.JSONDecodeError:
                contexto = {}

        # Renderizar template local
        html = render_local_template(mail.template, contexto)

        # Enviar correo vía SES
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
