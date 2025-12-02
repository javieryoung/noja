# mailer/ses.py
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def send_email_ses(to_email, subject, html_body, from_email="info@noja.young.uy", region="us-east-2", client=None):
    client = client or boto3.client("ses", region_name=region)
    response = client.send_email(
        Source=from_email,
        Destination={"ToAddresses": [to_email]},
        Message={
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {
                "Html": {"Data": html_body, "Charset": "UTF-8"},
                "Text": {"Data": "Texto alternativo", "Charset": "UTF-8"}
            }
        }
    )
    return {"status": "ok", "message_id": response["MessageId"]}