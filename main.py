import pyodbc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.db import connect,query
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
    sql = """select d.FNTEDCTO , d.NUMEDCTO , d.IDTERCERO , d.FECHDCTO , t.NOMBRETER 
                from DOCUMENT d 
                left join  TERCEROS t on t.IDTERCERO =d.IDTERCERO  
                where FNTEDCTO =?
                and NUMEDCTO = ?"""

    conn=connect()
    data = query(conn=conn, sql=sql,params=(fndcto.zfill(2),numedcto.zfill(10)))
    return data

if __name__=='__main__':
    app()
