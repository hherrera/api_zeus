from helpers.db import connectdb, query
from settings import settings

def getOrdersRelations(id: int = 0):
    data = []
    conn = None
    try:
        conn = connectdb(settings.DB_INVENTARIO)
        # Primera consulta
        sql1 = """
        SELECT Iden_documentosrelacionados as id, cast(importador as varchar) AS Documento, 'REMISION' AS TIPO_DOCUMENTO
        FROM DOCUMENTOSRELACIONADOS AS D
        LEFT OUTER JOIN PedidoDeCliente As P On D.Exportador = P.Consecutivo
        LEFT JOIN FacturaDeCliente fdc ON D.Importador = FDC.Consecutivo
        WHERE P.Consecutivo = ? and D.TipoImportador = 20
        """
        data1 = query(conn=conn, sql=sql1, params=(id,))
        if isinstance(data1, dict):
            data1 = [data1]
        if data1 is None: 
            data1= []   
        data.extend(data1)

        # Segunda consulta
        sql2 = """
        SELECT Iden_documentosrelacionados as id, FDC.Documento AS documento, 'FACTURA' AS TIPO_DOCUMENTO
        FROM DOCUMENTOSRELACIONADOS AS D
        LEFT OUTER JOIN PedidoDeCliente As P On D.Exportador = P.Consecutivo
        LEFT JOIN FacturaDeCliente fdc ON D.Importador = FDC.Consecutivo
        WHERE P.Consecutivo = ? and D.TipoImportador = 9
        """
        data2 = query(conn=conn, sql=sql2, params=(id,))
        if isinstance(data2, dict):
            data2 = [data2]
        if data2 is None: 
            data2= []   
        data.extend(data2)
    except Exception as e:
        print(f"Error al obtener relaciones de ordenes: {e}")
        # Aquí puedes decidir cómo manejar el error, por ejemplo, reintentar la conexión o simplemente registrar el error.
    finally:
        if conn:
            conn.close()  # Asegúrate de cerrar la conexión independientemente de si hubo una excepción o no.

    return data
