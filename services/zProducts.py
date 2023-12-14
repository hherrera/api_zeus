from helpers.db import connect,query, connectdb
from settings import settings

def  getProductsAll():
    
    conn=connectdb(settings.DB_INVENTARIO)
   
    sql = """Select  D.idArticulo as id,
                From Articulo As D 
                where substring(Grupo,1,2)='15' 
                order by id ASC """
    data = query(conn=conn, sql=sql)
        
    if isinstance(data, dict):
        data = [data]
    
    
    return data

def  getProductById(id:int):
    
    conn=connectdb(settings.DB_INVENTARIO)
    
    sql = """Select  D.idArticulo as id,
                From Articulo As D 
                where id =?
                 """
    data = query(conn=conn, sql=sql,params=(id,))

        
    if isinstance(data, dict):
        data = [data]
    
    
    return data

def  getProduct(product_id:int):
    
    sql = """Select  D.idArticulo, D.Nombre, D.codigo, D.grupo
        From	Articulo As D 
		  where D.idArticulo =? 
	     """
    
    conn=connectdb(settings.DB_INVENTARIO)
    data = query(conn=conn, sql=sql,params=(product_id,))
    
    return data

