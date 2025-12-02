# mailer/tests/test.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import json
import boto3
from botocore.stub import Stubber

from mailer.models import Mailer
from mailer.tasks import send_pending_mails_via_ses
from botocore.stub import Stubber, ANY

class TestSendPendingMails(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="tester@example.com",
            password="secret",
            nombre="Tester Name",
            pais="Uruguay",
        )
        self.mail = Mailer.objects.create(
            user=self.user,
            email="destinatario@example.com",
            subject="Correo pendiente",
            template="mailer/email_template.html",
            context=json.dumps({
                "subject": "Correo pendiente",   # ← agregado
                "texto": "Este es un correo pendiente",
                "button_url": "https://example.com",
                "button_text": "Ver más",
                "current_year": 2025,
                "brand_name": "Mi Marca"
            })
        )

    def test_send_pending_mail_marks_as_sent(self):
        client = boto3.client("ses", region_name="us-east-2")
        stubber = Stubber(client)

        expected_params = {
            "Source": "info@noja.young.uy",
            "Destination": {"ToAddresses": ["destinatario@example.com"]},
            "Message": {
                "Subject": {
                    "Data": "Correo pendiente",
                    # si tu código añade Charset, lo podés aceptar sin chequear valor
                    "Charset": ANY,
                },
                "Body": {
                    "Html": {
                        "Data": ANY,      # HTML completo del template, no lo validamos
                        "Charset": ANY,   # suele ser UTF-8
                    },
                    "Text": {
                        "Data": ANY,      # "Texto alternativo" u otro
                        "Charset": ANY,
                    },
                },
            },
        }

        stubber.add_response(
            "send_email",
            {"MessageId": "fake-id-123"},
            expected_params,
        )
        stubber.activate()

        enviados = send_pending_mails_via_ses(client=client)
        self.assertEqual(enviados, 1)

        self.mail.refresh_from_db()
        self.assertIsNotNone(self.mail.sent_on)