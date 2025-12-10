import requests

url = "http://ac29f9f9f63c4457c9520557b01bcab9-369530971.us-east-1.elb.amazonaws.com/resumen/latest"

headers = {
    "X-API-Key": "api-newscrapper-key01"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # lanza excepción si el status no es 200
    print("Status:", response.status_code)
    print("Respuesta JSON:", response.json())  # si el endpoint devuelve JSON
except requests.exceptions.RequestException as e:
    print("Error en la petición:", e)+591 