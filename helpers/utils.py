from datetime import datetime
from decimal import Decimal
def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
# Función de serialización para Decimals
def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # Convertir Decimal a cadena