from helpers.db import connect,query, connectdb
from settings import settings

def  getDispatchAll(CURRENT_SYNC:int=0):
    
    conn=connectdb(settings.DB_INVENTARIO)
    if CURRENT_SYNC==0:
        sql = """Select top 5  D.Consecutivo as id,D.Estado
                From Remision As D 
                where YEAR(D.Fecha) >= 2023
                order by D.Consecutivo ASC """
        data = query(conn=conn, sql=sql)

    else:
        sql = """Select top 5 D.Consecutivo as id,D.Estado
                From Remision As D 
                where  D.Consecutivo >= ? AND YEAR(D.Fecha) >= 2023
                order by D.Consecutivo ASC """
        data = query(conn=conn, sql=sql,params=(CURRENT_SYNC,))
        

    
    
    return data

def  getDispatch(dispatch_id:int):
    """Select Remision , con los Items en la data"""
    sql = """Exec spRptRemision ? 
	     """
    
    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(dispatch_id,))

    if isinstance(data, dict):
        data = [data]


    return data


def  getOrderItems(order_id:int):
      
    sql = """
       Select  DI.iden as id,DI.Codigo,D.Consecutivo,
		A.Codigo,A.Nombre As 'NombreArt',A.Presentacion,DI.PorcentajeDcto,DI.PorcentajeIVA,
		Abs(DI.Cantidad) As 'Cantidad', 
		Valorunidad = dbo.fnNuevaValorUnidad(0, DI.ValorUnidad, DI.ValorUnidad2)  
	From	PedidoDeCliente As D 
		LEFT OUTER JOIN DocumentoItems As DI	
		ON D.Consecutivo=DI.Documento And DI.TipoDocumento=7 
		LEFT OUTER JOIN Items As I ON DI.Item=I.Codigo 
		LEFT OUTER JOIN Articulo As A ON I.Articulo=A.IDArticulo 
       Where d.consecutivo = ? """
   
    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(order_id,))
     # Verificar si data es un dict y convertirlo a lista si es necesario
    if isinstance(data, dict):
        data = [data]
    return data