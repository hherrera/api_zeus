from datetime import datetime
from decimal import Decimal
def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
# Función de serialización para Decimals
def decimal_serializer(value):
    if isinstance(value, Decimal):
        return float(value)
    return value  # Convertir Decimal a cadena