from helpers.db import connect,query
from settings import settings


def getDocument(fndcto:str,numedcto:str):
    sql = """select d.FNTEDCTO , d.NUMEDCTO , d.IDTERCERO , d.FECHDCTO , t.NOMBRETER 
                from DOCUMENT d 
                left join  TERCEROS t on t.IDTERCERO =d.IDTERCERO  
                where FNTEDCTO =?
                and NUMEDCTO = ?"""

    conn=connect()
    data = query(conn=conn, sql=sql,params=(fndcto.zfill(2),numedcto.zfill(10)))
    return data

