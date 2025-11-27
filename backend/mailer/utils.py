import requests
from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from home.models import Suggestion

def send_daily_suggestions():
    # Filtrar sugerencias del día
    today_suggestions = Suggestion.objects.filter(date__date=now().date())

    if not today_suggestions.exists():
        return  # No enviar nada si no hay sugerencias

    # Contexto para el template
    context = {
        "suggestions": today_suggestions
    }

    # Renderizar template remoto con contexto
    html_content = render_remote_template(
        "https://tuservidor.com/templates/emails/suggestions.html",  # URL del template remoto
        context
    )

    # Construir y enviar el correo
    msg = EmailMultiAlternatives(
        subject="Sugerencias del día",
        body="Aquí están las sugerencias del día.",  # fallback en texto plano
        from_email="tuemail@dominio.com",
        to=["destinatario@dominio.com"],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def render_remote_template(template_url, context_dict):
    """
    Descarga un template remoto vía HTTP y lo renderiza con el contexto dado.
    """
    response = requests.get(template_url)
    response.raise_for_status()
    template_string = response.text
    template = Template(template_string)
    context = Context(context_dict)
    return template.render(context)