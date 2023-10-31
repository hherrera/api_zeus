import pyodbc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.zeus import getDocument
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
    data = None
    ## cadena conexion con 'Inventario_Ladrillera'
    str_conn1 = settings.database_url()
    dbname =  settings.DATABASE
    settings.DATABASE='Inventario_Ladrillera'
    str_conn2 = settings.database_url()
    settings.DATABASE=dbname
    print(str_conn1,str_conn2)
    conn1=connect(str_conn1)
    conn2=connect(str_conn2)
    
    ## buscar fuente
    sql = """select top 1 fuente from resolucionesdefacturas where prefijo =?
                """
    res = query(conn=conn1, sql=sql,params=(prefijo,))
    if res :
        fndcto = res['fuente']
        ## buscar factura 
        sql2 = """select top 1 f.documento, f.fuente, f.fecha, f.cliente , c.RAZONCIAL as nombre
                        from Facturadecliente f 
                        inner join CLIENTES c ON f.cliente = c.idcliente
                        where f.fuente = ? and f.documento = ?
                    """
        fac = query(conn=conn2, sql=sql2,params=(fndcto.zfill(2),numedcto.zfill(10) ))
        
        if fac:

            data ={"prefijo": prefijo,
                "fuente":fndcto,
                "documento": fac['documento'] ,
                "fecha": fac['fecha'] ,
                "cliente": fac['cliente'] ,
                "nombre": fac['nombre'] 
                }
        
    return data

@app.get("/nomina/contrato/{code}")
async def get_empleado(code:str):
    data = None
    ## cadena conexion con 'Inventario_Ladrillera'
    settings.DATABASE='Nomina'
    str_conn = settings.database_url()
    conn=connect(str_conn)

    sql="""select nc.Codigo  as code, ne.Identificacion as iden , ne.Nombres as name, ne.FechaNacimiento as birthdate, ne.Email as email
        from Nomina.dbo.Nm_Contrato nc 
        inner join Nomina.dbo.Nm_Empleado ne on nc.IDEN_Empleado = ne.IDEN  
        where nc.Codigo =?
    """
    res = query(conn=conn, sql=sql,params=(code,))
    print(res)
    if res:
        data = {
            "code" : res['code'],
            "iden" : res['iden'],
           "name" : res['name'],
           "email" : res['email'],
           "birthdate" : res['birthdate'],
        }
    return data
if __name__=='__main__':
    app()
