from helpers.db import connect,query, connectdb
from settings import settings

def  getDispatchAll(CURRENT_SYNC:int=0):
    
    conn=connectdb(settings.DB_INVENTARIO)
    if CURRENT_SYNC==0:
        sql = """Select D.Consecutivo as id,D.Estado
                From Remision As D 
                where YEAR(D.Fecha) >= 2023
                order by D.Consecutivo ASC """
        data = query(conn=conn, sql=sql)

    else:
        sql = """Select  D.Consecutivo as id,D.Estado
                From Remision As D 
                where  D.Consecutivo >= ? AND YEAR(D.Fecha) >= 2023
                order by D.Consecutivo ASC """
        data = query(conn=conn, sql=sql,params=(CURRENT_SYNC,))
    
    if isinstance(data, dict):
        data = [data]
    
    return data

def  getRptDispatch(dispatch_id:int):
    """Select Remision , con los Items en la data"""
    sql = """Exec spRptRemision ? 
	     """
    
    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(dispatch_id,))

    if isinstance(data, dict):
        data = [data]


    return data


def  getDispatch(dispatch_id:int):
    
    sql = """
        Select  D.Consecutivo as id,D.Fecha,D.Detalle,D.Estado,D.Cliente,CL.IDTercero,D.Facturada ,D.despachotransportadora, D.DespachoDireccion , D.DespachoCiudad ,
		CL.RazonCial ,CL.Direccion,CL.Ciudad,CL.Telefono,D.Vendedor,V.NOMBVENDE, DR.Exportador as pedido
        From	Remision As D 
		LEFT OUTER JOIN Clientes As CL ON D.Cliente=CL.IDCliente 
		LEFT OUTER JOIN MAEVENDE AS V ON D.Vendedor=V.IDVende
		LEFT OUTER JOIN DOCUMENTOSRELACIONADOS AS DR 
				ON DR.TipoImportador=20 AND DR.Importador=D.Consecutivo 
        where D.consecutivo =?
	     """
    
    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(dispatch_id,))
    if isinstance(data, dict):
        data = [data]
    return data


def  getDispatchItems(order_id:int):
      
    sql = """
       Select  DI.iden as id,DI.Codigo,D.Consecutivo,
		A.Codigo,A.Nombre As 'NombreArt',A.Presentacion,DI.PorcentajeDcto,DI.PorcentajeIVA,
		Abs(DI.Cantidad) As 'Cantidad', 
		Valorunidad = dbo.fnNuevaValorUnidad(0, DI.ValorUnidad, DI.ValorUnidad2)  ,
        DI.preciounidad, DI.preciototal
	From	Remision As D 
		LEFT OUTER JOIN DocumentoItems As DI	
		ON D.Consecutivo=DI.Documento And DI.TipoDocumento=20 
		LEFT OUTER JOIN Items As I ON DI.Item=I.Codigo 
		LEFT OUTER JOIN Articulo As A ON I.Articulo=A.IDArticulo 
       Where d.consecutivo = ? """
   
    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(order_id,))
     # Verificar si data es un dict y convertirlo a lista si es necesario
    if isinstance(data, dict):
        data = [data]
    return data