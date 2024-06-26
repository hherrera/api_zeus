from helpers.db import connectdb,query
from settings import settings
from datetime import datetime
def  getCreditLimitForClient(client_id:str):
    try:
        sql = """exec SpRptCuposDeClientes ?, ?  """

        conn=connectdb(settings.DB_INVENTARIO)
        data = query(conn=conn, sql=sql,params=(client_id,client_id))
        # Verificar si data es un dict y convertirlo a lista si es necesario
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception as e:
        print("Error:", e)
        return {"error": "An error occurred while processing your request."}

def  getAccountBalanceForClient(code:str,client_id:str):
    current_period = datetime.now().strftime('%Y%m')
    sql =f""" select codicta,auxiaux,sdanaux,mvdbaux,mvcraux,sdacaux
            from saldoaux_bu
            where 
            CODICTA =? 
            and AUXIAUX =?
            and ANOAUX = ?
            and BU='Local'
            """
    try:
        conn=connectdb(settings.DB_CONTABILIDAD)
        data = query(conn=conn, sql=sql,params=(code,client_id, current_period))
        # Verificar si data es un dict y convertirlo a lista si es necesario
        if isinstance(data, dict):
            data = [data]
        
    except Exception as e:
        print("Error:", e)
        return {"error": "An error occurred while processing your request."}
    return data

