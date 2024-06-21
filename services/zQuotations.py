from helpers.db import connect,query, connectdb
from settings import settings

def  getRptSalesFormat(consecutive:int, tipo_doc:int):
    
    conn=connectdb(settings.DB_INVENTARIO)
    campos = ["codigoitem", "nombreitem", "presentacion", "codigolote", "cantidad", "precioenotramoneda", "porcentajedcto", "porcentajeiva", "totalbruto", "itemsdetalle", "tipo","bodega" ,"ordengrabacion"]

    sql = """exec SpRptFormatoVentasMejorado_Nuevo ?, ?  """
    data = query(conn=conn, sql=sql,params=(consecutive,tipo_doc))
    
    print(data) 
    if isinstance(data, dict):
        data = [data]
    header = data[0]
    
      # Remover los campos especificados en `campos` de `header`
    header_ = {k: v for k, v in header.items() if k not in campos}

    items = data
    # Filtrar los diccionarios en la lista items
    items_ = [{campo: item[campo] for campo in campos} for item in items]


    sql = """  exec SpRptCuotas ?,'A Credito', ?  """
    cuotas = query(conn=conn, sql=sql,params=(consecutive,tipo_doc))
        
    if isinstance(cuotas, dict):
        cuotas = [cuotas]
  


    """ @numerofactura left('Nº Documento'+space(17),17)+':' +{SpRptFormatoVentasMejorado_Nuevo.Fuente} + ' - '+ {SpRptFormatoVentasMejorado_Nuevo.Documento}"""
    """ @ left('Nº Interno'+space(17),17)+':' + Cstr({SpRptFormatoVentasMejorado_Nuevo.Consecutivo}, "0")
"""
    return {"header":header_,"items":items_,"cuotas":cuotas}