import boto3
from botocore.exceptions import BotoCoreError, ClientError

def send_email_ses(to_email, subject, html_body,
                   from_email="info@noja.young.uy", region="us-east-2"):
    client = boto3.client("ses", region_name=region)
    try:
        response = client.send_email(
            Source=from_email,
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Html": {"Data": html_body},
                    "Text": {"Data": "Este correo requiere un cliente compatible con HTML."}
                }
            }
        )
        return {"status": "ok", "message_id": response["MessageId"]}
    except (BotoCoreError, ClientError) as e:
        return {"status": "error", "details": str(e)}