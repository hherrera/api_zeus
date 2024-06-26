from services.zOrders import getOrdersAll, getOrderItems, getOrder,getOrderById
from services.zDispatch import getDispatch,getDispatchItems,getDispatchAll
from services.zProducts import getProductsAll, getProduct
from services.zDocsRelations import getOrdersRelations
from crud.orders import upsertOrder,upsertItemOrder,fetchOrdersbyStatus, deleteItemsOrder
from crud.dispatchs import upsertDispatch,upsertItemDispatch, fetchDispatchbyStatus, deleteDispatchsOrders,insertDispatchsOrders
from crud import parameters  
from crud.products import upsertProducts
from crud.orders import upsertOrderDocRelations
from helpers.utils import datetime_serializer, decimal_serializer

def sync_products():
    num=0
    products = getProductsAll()

    for product in products:
        p = getProduct(product['id'])
        print(p)
        #D.idArticulo, D.Nombre, D.codigo, D.grupo
        upsertProducts({"id":int(product['id']),
                        "name":p['nombre'],
                        "code":p['codigo'],
                        "group_id":p['grupo'],
                        "display": p['presentacion']
                        })
        num=num+1
    return num


def sync_dispatch(type:str):
    num=0
    # buscar contador actual de orders
    
    
    # cargar todas las orders 
    if type=="All":
        print(f"Actualizando todos los Pedidos!!!!! ") 
        dispatchs = getDispatchAll(0)  
    elif type=='Status':
        dispatchs=fetchDispatchbyStatus(['Pendiente','Parcialmente Satisfecho'])
    elif type=='New':
            param = parameters.select('CURRENT_DISPATCH_SYNC')[0]
            current_id = int(param['value'])  
            print(f"Actualizando desde la remision #{current_id}") 
            dispatchs = getDispatchAll(current_id)
    
    
    else:
        return False
    
    
    # recorrer orders
    for dispatch in dispatchs:
        print(dispatch)
        #cargar order
        d_id=int(dispatch['id'])
        # pueden ser varios pedidos
        dispatch_a=getDispatch(d_id) 
        dispatch_=dispatch_a[0]
        
        #crear dict order

        print(f"Remision #{d_id}")
        dispatch_dict = {
            "id": d_id,
            "date":datetime_serializer(dispatch_['fecha']),
            "details": dispatch_['detalle'],
            "status": dispatch_['estado'],
            "client_id":dispatch_['cliente'],
            "client_name": dispatch_['razoncial'],
            "client_address": dispatch_['direccion'],
            "client_city": dispatch_['ciudad'],
            "client_phone": dispatch_['telefono'],
            "seller_id": dispatch_['vendedor'],
            "seller_name": dispatch_['nombvende'],
            "dispatch_address":dispatch_['despachodireccion'],
            "dispatch_city": dispatch_['despachociudad'],
            "dispatch_details": dispatch_['despachotransportadora']
            
            
         }
     

        #cargar items
        items = getDispatchItems(d_id)

        #crear dict item dispatch_data -> json, si es necesario guardar los items de la remision
        # Filtrar la lista para excluir elementos con "codigoitem" igual a 0
        
        
        #crear dict item
        items_data = []
        for item in items:
            
            if item['id'] is None:
                continue
            qty = decimal_serializer(item['cantidad']) 
            val = decimal_serializer(item['preciounidad']) 
           
            desc = decimal_serializer(item['porcentajedcto'])
            tot = decimal_serializer(item['preciototal']*(1-item['porcentajedcto']/100))
            print(tot)
            item_dict= {"id":int(item['id']),
                        "dispatch_id": int(item['consecutivo']),
                        "item_code": item['codigo'],
                        "item_name": item['nombreart'],
                        "quantity": qty,
                        "value": val,
                        "display":item['presentacion'] ,
                        "subtotal":tot
                        }
            
            items_data.append(item_dict)

        #upsert order & item
        
        result_ = upsertDispatch(dispatch_dict)
        result_items = upsertItemDispatch(items_data)
        #actualizar remisiones/pedidos
        result = deleteDispatchsOrders(int(d_id))
        for dp in dispatch_a:
            #actualizar pedido
          if dp['pedido']  is None:
            continue       
          if sync_orders('One', int(dp['pedido'])) is not None:
            res=insertDispatchsOrders({"dispatch_id":int(d_id),"order_id":int(dp['pedido'])})
        
        
        #actualizar contador con order_id
        if type=='New' :
            parameters.update('CURRENT_DISPATCH_SYNC',int(d_id))
        num=num+1
    return num





def sync_orders(type:str, id:int=None):
    num=0
    # buscar contador actual de orders
    
    if type=='Status':
        orders=fetchOrdersbyStatus(['Pendiente','Parcialmente Satisfecho'])
    elif type =='All':
        # cargar todas las orders 
        print(f"Actualizando todos los Pedidos!!!!! ") 
        
        orders = getOrdersAll(0)  
        print(f"Actualizando todos los Productos!!!!! ") 
        sync_products()
    elif type=='New':
            param = parameters.select('CURRENT_ORDER_SYNC')[0]
            current_id = int(param['value'])  
            print(f"Actualizando desde el Pedido #{current_id}") 
            orders = getOrdersAll(current_id)
    elif type =='One':
        # cargar todas las orders 
        print(f"Actualizando un Pedido!!!!! ") 
        orders = getOrderById(id)  
    else:
        return False
  
            
    #print(orders)
    if orders is None:
        return None     
    # recorrer orders
    for order in orders:
        order_id =int(order['id'])
        #cargar order
        order_data=getOrder(order_id)  
        #crear dict order
        if order_data is None:
            continue
       
        print(f"Pedido #{order_id}")
        order_dict = {
            "id":order_id,
            "date":datetime_serializer(order_data['fecha']),
            "delivery_date": datetime_serializer(order_data['fechaentrega']),
            "details": order_data['detalle'],
            "status": order_data['estado'],
            "client_id":order_data['cliente'],
            "client_name": order_data['razoncial'],
            "client_address": order_data['direccion'],
            "client_city": order_data['ciudad'],
            "client_phone": order_data['telefono'],
            "seller_id": order_data['vendedor'],
            "seller_name": order_data['nombvende'],
            "delivery_address": order_data.get('despachodireccion',''),
            "delivery_city": order_data.get('despachociudad',''),
            "delivery_reference": order_data.get('despachocliente','')

         }
        
        print(order_dict)
        #cargar items
        items = getOrderItems(order['id'])
        #crear dict item
        items_data = []
        for item in items:
            print(item)
            if item['id'] is None:
                continue
            item_dict= {"id":int(item['id']),
                        "order_id": int(item['consecutivo']),
                        "item_code": item['codigo'],
                        "item_name": item['nombreart'],
                        "quantity": int(item['cantidad']),
                        "value": int(item['preciounidad']) ,
                        "missing_quantity": int(item['faltantes']) ,
                        "display":item['presentacion'] 
                       
                        }
            items_data.append(item_dict)
        #upsert order & item
        result_order = upsertOrder(order_dict) 
        # borrar los items
        result_delete =deleteItemsOrder(order_id)  
        result_items = upsertItemOrder(items_data)
        #actualizar contador con order_id

        order_docs_data =  getOrdersRelations(order['id'])
        for order_rel in  order_docs_data:
            upsertOrderDocRelations({
                 "id":int(order_rel['id']),
                 "order_id":int(order['id']),
                 "doc_id":order_rel['documento'],
                "tipo_doc":order_rel['tipo_documento'],

                                      })



        if (type=='New'):
            parameters.update('CURRENT_ORDER_SYNC',int(order['id']))
        num=num+1
    return num

if __name__=='__main__':
    sync_orders()