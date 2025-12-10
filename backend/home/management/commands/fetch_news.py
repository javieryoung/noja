import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from home.models import New, Suggestion


class Command(BaseCommand):
    help = "Fetch news from API and store them in New and Suggestion models"

    def handle(self, *args, **options):
        url = "http://35.169.240.172:8000/resumen/latest"
        headers = {
            "X-API-Key": "api-newscrapper-key01"
        }
        requests.packages.urllib3.util.connection.HAS_IPV6 = False

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            self.stdout.write(self.style.SUCCESS(f"Status: {response.status_code}"))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error en la petición: {e}"))
            return

        data = response.json()
        for art in data.get("articulos", []):
            # Separar title en primera palabra y resto
            words = art["title"].split(" ", 1)
            title = words[0]
            subtitle = art["title"]

            # Limpiar summary
            summary = art.get("summary", "")
            if summary.startswith("Resumen:"):
                summary = summary.replace("Resumen:", "", 1).strip()

            # Extraer tickers
            symbol = ""
            if "Tickers:" in summary:
                parts = summary.split("Tickers:")
                content = parts[0].strip()
                symbol = parts[1].strip()
            else:
                content = summary.strip()

            # Guardar en modelo New
            new_obj = New.objects.create(
                title=title,
                subtitle=subtitle,
                content=content,
                date=art.get("published", timezone.now())
            )

            # Guardar Suggestion si hay símbolos
            if symbol:
                for s in symbol.split(","):
                    s_clean = s.strip()
                    if s_clean:
                        Suggestion.objects.create(
                            new=new_obj,
                            symbol=s_clean,
                            title=subtitle,
                            date=timezone.now(),
                        )