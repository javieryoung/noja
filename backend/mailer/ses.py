import boto3
from botocore.exceptions import BotoCoreError, ClientError

def send_email_ses(
    to_email,
    subject,
    html_body,
    from_email="noreply@noja.young.uy",
    region="us-east-2",
    client=None
):
    client = client or boto3.client("ses", region_name=region)
    try:
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

    except ClientError as e:
        # Errores específicos de SES (ej: MessageRejected, Throttling, etc.)
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        return {
            "status": "error",
            "error_code": error_code,
            "details": error_message
        }

    except BotoCoreError as e:
        # Errores de boto3 (problemas de conexión, credenciales, etc.)
        return {
            "status": "error",
            "error_code": "BotoCoreError",
            "details": str(e)
        }

    except Exception as e:
        # Cualquier otro error inesperado
        return {
            "status": "error",
            "error_code": "UnknownError",
            "details": str(e)
        }