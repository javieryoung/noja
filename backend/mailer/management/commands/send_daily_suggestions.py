from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from mailer.models import Mailer
from home.models import Suggestion, CustomUser

class Command(BaseCommand):
    help = "Crea entradas Mailer para las sugerencias del día"

    def handle(self, *args, **options):

        today = timezone.now().date()  # fecha en UTC
        start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        suggestions = Suggestion.objects.filter(date__gte=start, date__lt=end)

        if not suggestions.exists():
            self.stdout.write("No hay sugerencias para hoy.")
            return  # 🚫 no crea nada

        html = render_to_string("mailer/suggestions.html", {"suggestions": suggestions})
        subject = "Sugerencias del día"

        subscribers = CustomUser.objects.filter(is_active=True)
        created = 0

        for u in subscribers:
            self.stdout.write(f"- {u.id} {u.email}")
            Mailer.objects.create(
                email=u.email,
                user=u,
                subject=subject,
                context={"html": html, "created_at": str(timezone.now())},
                template="mailer/suggestions.html",
            )
            created += 1

        self.stdout.write(f"Creadas {created} entradas Mailer para sugerencias.")