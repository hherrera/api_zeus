from helpers.db import connect,query, connectdb
from settings import settings

def  getOrdersAll(CURRENT_ORDER_SYNC:int=0):
    
    conn=connectdb(settings.DB_INVENTARIO)
    if CURRENT_ORDER_SYNC==0:
        sql = """Select  D.Consecutivo as id,D.Estado
                From PedidoDeCliente As D 
                where YEAR(D.Fecha) > 2023
                order by D.Consecutivo ASC """
        data = query(conn=conn, sql=sql)

    else:
        sql = """Select  D.Consecutivo as id,D.Estado
                From PedidoDeCliente As D 
                where  D.Consecutivo >= ? AND YEAR(D.Fecha) > 2023
                order by D.Consecutivo ASC """
        data = query(conn=conn, sql=sql,params=(CURRENT_ORDER_SYNC,))
        
    if isinstance(data, dict):
        data = [data]
    
    
    return data

def  getOrderById(id:int):
    
    conn=connectdb(settings.DB_INVENTARIO)
    
    sql = """Select  D.Consecutivo as id,D.Estado
                From PedidoDeCliente As D 
                where D.consecutivo=?
                 """
    data = query(conn=conn, sql=sql,params=(id,))

        
    if isinstance(data, dict):
        data = [data]
    
    
    return data

def  getOrder(order_id:int):
    
    sql = """Select  D.Consecutivo as id,D.Fecha,D.FechaEntrega,D.Detalle,D.Estado,D.Cliente,CL.IDTercero,
		CL.RazonCial ,CL.Direccion,CL.Ciudad,CL.Telefono,D.Vendedor,V.NOMBVENDE, D.DespachoDireccion, D.DespachoCliente, D.DespachoCiudad
        From	PedidoDeCliente As D 
		LEFT OUTER JOIN Clientes As CL ON D.Cliente=CL.IDCliente 
		LEFT OUTER JOIN MAEVENDE AS V ON D.Vendedor=V.IDVende
        where D.consecutivo =? 
	     """
    
    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(order_id,))
    
    return data


def  getOrderItems(order_id:int):
      
    sql = """
       Select  DI.iden as id,DI.Codigo,D.Consecutivo,
		A.Codigo,A.Nombre As 'NombreArt',A.Presentacion,DI.PorcentajeDcto,DI.PorcentajeIVA,
		Abs(DI.Cantidad) As 'Cantidad', 
		Valorunidad = dbo.fnNuevaValorUnidad(0, DI.ValorUnidad, DI.ValorUnidad2)  
        PrecioUnidad as precio, 
        faltantes,
        aprobados
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