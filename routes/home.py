from fastapi import APIRouter, HTTPException, Depends, Path, Body
from fastapi.responses import JSONResponse
from pydantic.types import List
from settings import Settings

from services.zeus import getDocument, getInvoice, getEmpleado
from services.takephotos import takephoto
from settings import settings
from dependencies import get_token_header
from commands.sync import sync_orders

router = APIRouter()

settings = Settings()

# Dependencia para validar el token en la ruta /syncronize
async def verify_token(x_token: str = Depends(get_token_header)):
    return x_token

@router.get("/")
def home():
    """ """ 
    return {
        "PROJECT_NAME":settings.PROJECT_NAME ,
        "PROJECT_VERSION":settings.PROJECT_VERSION
        }


@router.get("/document/{fndcto}/{numedcto}")
async def get_doc_metadata(fndcto:str,numedcto:str):
    data = getDocument(fndcto,numedcto)
    return data

@router.get("/invoice/{prefijo}/{numedcto}")
async def get_inv_metadata(prefijo:str,numedcto:str):
    data = getInvoice(prefijo=prefijo,numedcto=numedcto)
    return data

@router.get("/nomina/contrato/{code}")
async def get_empleado(code:str):
    data = getEmpleado(code=code)
    return data


@router.post("/syncronize/new")
async def sync_orders_new(x_token: str = Depends(verify_token)):
    data = sync_orders(type='New')
    #data = sync_orders(type='Status')

    return  {"success":True}

