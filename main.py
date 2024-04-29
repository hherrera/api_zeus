import pyodbc
from fastapi import FastAPI,Depends, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from services.cameras import Camera
from crud.cameras import fecthCamerabyDoorId

from services.zeus import getDocument, getInvoice, getEmpleado
from services.takephotos import takephoto
from services.reports import fetch_trucks_control, fetch_loading_distribution, fetch_order_information, fetch_vehicle_control, fetch_load_report_driver_by_month

from settings import settings
from dependencies import get_token_header
from commands.sync import sync_orders

from routes import home

from models.reports import ReportControlRequest, ReportDriversRequest


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

# includes routes
#app.include_router(home.router)


@app.get("/")
def home():
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

@app.post("/make_report_control/")
async def make_report_control(request_data:ReportControlRequest,x_token: str = Depends(verify_token)):
   # Extraer date_ref y emails del objeto request_data
    date_ref = request_data.date_ref
    emails = request_data.emails
    result = fetch_trucks_control(date_ref,emails)
    return result

@app.post("/make_report_vehicle/")
async def make_report_control(request_data:ReportControlRequest,x_token: str = Depends(verify_token)):
   # Extraer date_ref y emails del objeto request_data
    date_ref = request_data.date_ref
    emails = request_data.emails
    result = fetch_vehicle_control(date_ref,emails)
    return result
#fetch_loading_distribution  
@app.post("/make_report_loading_distribution/")
async def make_report_loading_distribution(request_data:ReportControlRequest,x_token: str = Depends(verify_token)):
   # Extraer date_ref y emails del objeto request_data
    date_ref = request_data.date_ref
    emails = request_data.emails
    result = fetch_loading_distribution(date_ref,emails)
    return result

# Reporte de programacion diaria
@app.post("/make_report_daily_programming/")
async def make_report_order_information(request_data:ReportControlRequest,x_token: str = Depends(verify_token)):
   # Extraer date_ref y emails del objeto request_data
    date_ref = request_data.date_ref
    emails = request_data.emails
    result = fetch_order_information(date_ref,emails)
    return result

# Reporte de incentivos conductores
@app.post("/make_report_driver_load/")
async def make_report_driver_load(request_data:ReportDriversRequest,x_token: str = Depends(verify_token)):
   # Extraer date_ref y emails del objeto request_data
    year_ref = request_data.year_ref
    month_ref = request_data.month_ref
    emails = request_data.emails
    result = fetch_load_report_driver_by_month(year=year_ref, month=month_ref,emails=emails)
    return result

if __name__=='__main__':
    app()
