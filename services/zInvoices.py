from helpers.db import connect,query
from settings import settings

def  getInvoicesAll(CURRENT_INVOICES_SYNC:int):
    
    sql = """Select D.Consecutivo,D.Fecha,D.Fuente,D.Serie,D.Documento,D.Cliente,Cl.RazonCial,D.Vendedor,V.NOMBVENDE,
			D.FormaPago,D.DiasCreditos,D.VencimientoInicial,D.Moneda,Total=sum(DI.Cantidad*DI.PrecioUnidad),TDCTO=sum(DI.Cantidad*DI.PrecioUnidad*DI.PorcentajeDCTO/100),TIVA=sum(DI.cantidad*DI.PrecioUnidad*(1-DI.PorcentajeDcto/100)*DI.PorcentajeIVA/100),
			GrupoP=D.FormaPago
		From FacturaDeCliente As D INNER JOIN DocumentoItems As DI ON D.Consecutivo=DI.Documento And DI.TipoDocumento=9
					     INNER JOIN Items As I ON DI.Item=I.Codigo
					     LEFT OUTER JOIN Clientes AS CL ON D.Cliente=Cl.IDCliente
					     LEFT OUTER JOIN MAEVENDE AS V ON D.Vendedor=V.IDVENDE
		where convert(smalldatetime,Fecha,111) Between Convert(smalldatetime,@FechaI,111)And Convert(smalldatetime,@FechaF,111)And
			Estado<>'Revertido' And Estado<>'Reversion'
		Group By D.Consecutivo,D.Fecha,D.Fuente,D.Serie,D.Documento,D.Cliente,Cl.Razoncial,D.Vendedor,V.NOMBVende,D.FormaPago,D.DiasCreditos,D.VencimientoInicial,D.Moneda"""

    conn=connect()
    data = query(conn=conn, sql=sql,params=(CURRENT_INVOICES_SYNC,))
    return data

def  getInvoice(consecutive:int):
    
    sql = """Select  D.Consecutivo,D.Fecha,D.FechaEntrega,D.Detalle,D.Estado,D.Cliente,CL.IDTercero,
		CL.RazonCial ,CL.Direccion,CL.Ciudad,CL.Telefono,D.Vendedor,V.NOMBVENDE
        From	PedidoDeCliente As D 
		LEFT OUTER JOIN Clientes As CL ON D.Cliente=CL.IDCliente 
		LEFT OUTER JOIN MAEVENDE AS V ON D.Vendedor=V.IDVende
        where D.consecutivo =?
	    order by D.Consecutivo DESC """

    conn=connect()
    data = query(conn=conn, sql=sql,params=(consecutive,))
    return data


def  getInvoiceItems(consecutive:int):
   
    libro= 'L'#dbo.fnLibroActual() 
    origen_val = 0 #
    sql = """
       Select  DI.Codigo,D.Consecutivo,
		A.Codigo,A.Nombre As 'NombreArt',A.Presentacion,DI.PorcentajeDcto,DI.PorcentajeIVA,
		Abs(DI.Cantidad) As 'Cantidad', 
		Valorunidad = dbo.fnNuevaValorUnidad(?, DI.ValorUnidad, DI.ValorUnidad2)  

	From	PedidoDeCliente As D 
		LEFT OUTER JOIN DocumentoItems As DI	
		ON D.Consecutivo=DI.Documento And DI.TipoDocumento=7 
		LEFT OUTER JOIN Items As I ON DI.Item=I.Codigo 
		LEFT OUTER JOIN Articulo As A ON I.Articulo=A.IDArticulo 
       Where d.consecutivo = ? """

    conn=connect()
    data = query(conn=conn, sql=sql,params=(libro,origen_val,consecutive,))
    return data