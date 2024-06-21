from datetime import datetime
from decimal import Decimal

import requests

def check_url_existence(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
# Función de serialización para Decimals
def decimal_serializer(value):
    if isinstance(value, Decimal):
        return float(value)
    return value  # Convertir Decimal a cadena

# Función para convertir los tipos de datos no serializables a JSON
def default_converter(o):
    if isinstance(o, Decimal):
        return float(o)
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, bytes):
        return o.decode('utf-8')
    return str(o)