from pydantic import BaseModel, EmailStr, validator, Field
from typing import List, Optional
from datetime import date

# Modelo de solicitud para el endpoint
class ReportControlRequest(BaseModel):
    date_ref: Optional[str] = None  # Campo opcional para la fecha de referencia, por defecto es None
    start_date: Optional[str] = None  # Campo opcional para la fecha de inicio
    end_date: Optional[str] = None  # Campo opcional para la fecha de fin
    emails: List[EmailStr]  # Lista de correos electrónicos con validación

    # Validador para asegurarse de que la lista de emails no esté vacía
    @validator('emails')
    def check_emails_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('La lista de correos electrónicos no puede estar vacía')
        return v
class ReportDriversRequest(BaseModel):
    year_ref: int  # Campo para la año
    month_ref: int
    emails: List[EmailStr]  # Lista de correos electrónicos con validación

    # Opcional: Validador para asegurarse de que la lista de emails no esté vacía
    @validator('emails')
    def check_emails_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('La lista de correos electrónicos no puede estar vacía')
        return v