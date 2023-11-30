from services.zOrders import getOrdersAll, getOrderItems, getOrder
from services.zDispatch import getDispatch,getDispatchAll
from crud.orders import upsertOrder,upsertItemOrder,fetchOrdersbyStatus
from crud.dispatchs import upsertDispatch,upsertItemDispatch
from crud import parameters  
from helpers.utils import datetime_serializer, decimal_serializer





def sync_dispatch(all:bool=False):
    num=0
    # buscar contador actual de orders
    param = parameters.select('CURRENT_DISPATCH_SYNC')[0]
    
    current_id = int(param['value'])  
    print(f"Actualizando desde el Remision #{current_id}") 
    # cargar todas las orders 
    if all is True:
      orders = getDispatchAll(current_id)
    else:
      dispatchs = getDispatchAll(0)  
    # recorrer orders
    for dispatch in dispatchs:
        #cargar order
        d_id=int(dispatch['consecutive'])
        dispatch_data=getDispatch(d_id) 
        dispatch_=dispatch_data[0] 
        #crear dict order

        print(f"Remision #{d_id}")
        dispatch_dict = {
            "id": d_id,
            "date":datetime_serializer(dispatch_['fecha']),
            "details": dispatch_['detalle'],
            "status": dispatch_['estado'],
            "client_id":dispatch_['cliente'],
            "client_name": dispatch_['nombrecliente'],
            "client_address": dispatch_['direccioncli'],
            "client_city": dispatch_['ciudadcli'],
            "client_phone": dispatch_['telcli'],
            "seller_id": dispatch_['vendedor'],
            "seller_name": dispatch_['nombvende'],
            "dispatch_address":dispatch_['despachodireccion'],
            "dispatch_city": dispatch_['despachociudad'],
            "dispatch_details": dispatch_['despachotransportadora'],
            "order_id":dispatch_['pedido'],
            "zone_id":dispatch_['idzona'] 
         }
        #cargar items
        #items = getOrderItems(order['id'])

        #crear dict item dispatch_data -> json, si es necesario guardar los items de la remision
        # Filtrar la lista para excluir elementos con "codigoitem" igual a 0
        items = [elemento for elemento in dispatch_data if elemento["codigoitem"] != 0]
        
        #crear dict item
        items_data = []
        for item in items:
            print(item)
            if item['id'] is None:
                continue
            item_dict= {"id":int(item['id']),
                        "dispatch_id": int(item['consecutivo']),
                        "item_code": item['codigo'],
                        "item_name": item['nombreart'],
                        "quantity": decimal_serializer(item['cantidad']),
                        "value": item['valorunidad'] ,
                        "display":item['presentacion'] ,
                        "subtotal":decimal_serializer(item['valorunidad']*item['cantidad'])
                        }
            items_data.append(item_dict)

        #upsert order & item
        result_ = upsertDispatch(dispatch_dict)   
        result_items = upsertItemDispatch(items_data)
        #actualizar contador con order_id
        parameters.update('CURRENT_DISPATCH_SYNC',int(d_id))
        num=num+1
    return num





def sync_orders(type:str):
    num=0
    # buscar contador actual de orders
    
    if type=='Status':
        orders=fetchOrdersbyStatus(['Pendiente','Parcialmente Satisfecho'])
    elif type =='All':
        # cargar todas las orders 
        print(f"Actualizando todos los Pedidos!!!!! ") 
        orders = getOrdersAll(0)  
    elif type=='New':
            param = parameters.select('CURRENT_ORDER_SYNC')[0]
            current_id = int(param['value'])  
            print(f"Actualizando desde el Pedido #{current_id}") 
            orders = getOrdersAll(current_id)
    else:
        return False
  
            
    print(orders)
          
    # recorrer orders
    for order in orders:
        #cargar order
        order_data=getOrder(int(order['id']))  
        #crear dict order

        print(f"Pedido #{int(order['id'])}")
        order_dict = {
            "id": int(order_data['id']),
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
            "seller_name": order_data['nombvende']
         }
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
                        "value": item['valorunidad'] ,
                        "display":item['presentacion'] ,
                        "subtotal":item['valorunidad']*int(item['cantidad'])
                        }
            items_data.append(item_dict)
        #upsert order & item
        result_order = upsertOrder(order_dict)   
        result_items = upsertItemOrder(items_data)
        #actualizar contador con order_id
        if (type=='New'):
            parameters.update('CURRENT_ORDER_SYNC',int(order['id']))
        num=num+1
    return num

if __name__=='__main__':
    sync_orders()