from helpers.db import connectdb,query
from settings import settings

def  getInvoicesAll(CURRENT_INVOICES_SYNC:int):
    
    conn=connectdb(settings.DB_INVENTARIO)
    if CURRENT_INVOICES_SYNC==0:
        sql = """Select  D.Consecutivo as id,D.Estado
                From FacturaDeCliente As D 
                where YEAR(D.Fecha) >= 2023
                order by D.Consecutivo ASC """
        data = query(conn=conn, sql=sql)

    else:
        sql = """Select  D.Consecutivo as id,D.Estado
                From FacturaDeCliente As D 
                where  D.Consecutivo >= ? AND YEAR(D.Fecha) >= 2023
                order by D.Consecutivo ASC """
        data = query(conn=conn, sql=sql,params=(CURRENT_INVOICES_SYNC,))
        
    if isinstance(data, dict):
        data = [data]
    
    
    return data


def  getInvoice(consecutive:int):
    
    sql = """Select  D.Consecutivo, DR.Exportador as 'pedido',D.Fecha,D.VencimientoInicial ,D.Detalle,D.Estado,D.Cliente,CL.IDTercero,
		CL.RazonCial ,CL.Direccion,CL.Ciudad,CL.Telefono,D.Vendedor,V.NOMBVENDE
        From	FacturaDeCliente As D 
		LEFT OUTER JOIN Clientes As CL ON D.Cliente=CL.IDCliente 
		LEFT OUTER JOIN MAEVENDE AS V ON D.Vendedor=V.IDVende
		LEFT OUTER JOIN DOCUMENTOSRELACIONADOS AS DR 
				ON DR.TipoImportador=9 AND DR.Importador=D.Consecutivo 
        where D.consecutivo =? """

    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(consecutive,))
    return data


def  getInvoiceItems(consecutive:int):
   
   
    sql = """
 Select  DI.iden as id,DI.Codigo,D.Consecutivo,
		A.Codigo,A.Nombre As 'NombreArt',A.Presentacion,DI.PorcentajeDcto,DI.PorcentajeIVA,
		Abs(DI.Cantidad) As 'Cantidad', 
		Valorunidad = dbo.fnNuevaValorUnidad(0, DI.ValorUnidad, DI.ValorUnidad2)  
	From	FacturaDeCliente  As D 
		LEFT OUTER JOIN DocumentoItems As DI	
		ON D.Consecutivo=DI.Documento And DI.TipoDocumento=9
		LEFT OUTER JOIN Items As I ON DI.Item=I.Codigo 
		LEFT OUTER JOIN Articulo As A ON I.Articulo=A.IDArticulo 
       Where d.consecutivo =?
       """

    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(consecutive,))
     # Verificar si data es un dict y convertirlo a lista si es necesario
    if isinstance(data, dict):
        data = [data]
    return data