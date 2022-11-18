import pyodbc
from services.db import connect,query


#conn = connect()

conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=127.0.0.1;'
    r'DATABASE=Contabilidad_Ladrillera;'
    r'UID=sainventario;'
    r'PWD=z;'
    r'PORT=51433;'
    r'Trusted_Connection=yes;'
)
print(conn_str)
conn =pyodbc.connect(conn_str)

print(query(sql="select top 1 * from document", conn=conn))

