
from typing import Dict
import pyodbc

from settings import settings

def connectdb(dbname: str = None):
    if dbname is None:
        conn_str = settings.database_url()
    else:
        conn_str = settings.database_url(dbname=dbname)
    
    return pyodbc.connect(conn_str)




#crear la conexion con base a los parametros
def connect(conn_str: str = None):
    if conn_str is None:
        conn_str = settings.database_url()
        
    return pyodbc.connect(conn_str)
    
def row_to_dict(row):
    columns = [column[0].lower() for column in row.description] 
    return dict(zip(columns, row.fetchone()))
def rows_to_dict(row):
    columns = [column[0].lower() for column in row.description] 
    return [dict(zip(columns, row)) for row in row.fetchall()]

def query(sql : str, params : tuple = None, conn = None):
    conn_close=False
    results= None
    if conn is None:
        conn = connect()
        conn_close = True
   
    try:
        cur = conn.cursor()
        
        #print(f'sql:{sql} \n params:{params}')

        if params:
            row = cur.execute(sql,params)
        else:
            row = cur.execute(sql)
        results = rows_to_dict(row)
    except pyodbc.Error as e:
        ## responder Null
        print(f'Error {e} | SQL was {sql}, severity="ERROR"')
        
    finally:
        cur.close()
        if conn_close:
            conn.close()
    if not results:
        return None
    if len(results)==1: 
        return results[0]
    
    return results


if __name__=="__main__":
   pass


