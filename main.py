import pyodbc
from fastapi import FastAPI,Depends, HTTPException
from services.cameras import Camera
from fastapi.middleware.cors import CORSMiddleware
from services.zeus import getDocument, getInvoice, getEmpleado
from services.takephotos import takephoto
from crud.cameras import fecthCamerabyDoorId
from settings import settings
from dependencies import get_token_header
from commands.sync import sync_orders
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
# Dependencia para validar el token en la ruta /syncronize
async def verify_token(x_token: str = Depends(get_token_header)):
    return x_token


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


@app.post("/syncronize/new")
async def sync_orders_new(x_token: str = Depends(verify_token)):
    data = sync_orders(type='New')
    #data = sync_orders(type='Status')

    return  {"success":True}



# /inflow/:id/cam/:id
# recibe cam, 

@app.post("/cam/{inflow_id}/{door_id}/{action}/")
async def get_cam_frame(inflow_id:int,door_id:int,action:str, x_token: str = Depends(verify_token)):
    
    
    cams = fecthCamerabyDoorId(door_id)
     
    for item in cams:
        camera_id = item.get("id")
       
        if camera_id is not None :
            takephoto(cam = Camera(item.get("rstp")), inflow_id=inflow_id, action=action)
       

    return  {"success":True}

if __name__=='__main__':
    app()
