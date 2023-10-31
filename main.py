import pyodbc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.zeus import getDocument, getInvoice, getEmpleado
from settings import settings

print(settings.database_url())
app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    """ """ 
    return {
        "PROJECT_NAME":settings.PROJECT_NAME ,
        "PROJECT_VERSION":settings.PROJECT_VERSION
        }


@app.get("/document/{fndcto}/{numedcto}")
async def get_doc_metadata(fndcto:str,numedcto:str):
    data = getDocument(fndcto,numedcto)
    return data

@app.get("/invoice/{prefijo}/{numedcto}")
async def get_inv_metadata(prefijo:str,numedcto:str):
    data = getInvoice(prefijo=prefijo,numedcto=numedcto)
    return data

@app.get("/nomina/contrato/{code}")
async def get_empleado(code:str):
    data = getEmpleado(code=code)
    return data

if __name__=='__main__':
    app()
