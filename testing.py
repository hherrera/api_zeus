import json
from services.zOrders import getOrdersAll, getOrder, getOrderItems
from services.zDispatch import getDispatchAll, getDispatch
from commands.sync import sync_orders , sync_dispatch, sync_products
from crud.orders import fetchOrdersbyStatus
from crud.cameras import fecthCamerabyId
from services.zQuotations import getRptSalesFormat
from reports.quotations import rpt_quotation_format
from helpers.utils import default_converter
#import debugpy
# Habilita la depuración en el puerto 5679
#debugpy.listen(('0.0.0.0', 5678))

#response = getOrdersAll(0)
#response = getDispatchAll(0)
#print(response)
#print(getDispatch(17196))


#order = getOrder(1016999)
#items= getOrderItems(1016999)

## una vez al dia - sincronizar desde la app 
#sync_products()


### esto cada 5 minutos PEDIDOS
#data = sync_orders(type='New')
#print(data)

#data = sync_orders(type='Status')
#print(data)

## cada 5 minutos REMISIONES
#data = sync_dispatch(type='New')
#print(data)

#data =fetchOrdersbyStatus(['Pendiente','Parcialmente Satisfecho'])
#print(data)
#print(int(data[0]['id']))

#data = fecthCamerabyId(1)
#print(data)
#print(data[0]['rstp'])
#print(order)

data = getRptSalesFormat(1816, 23)
# Convertir el diccionario a JSON bonito
json_pretty = json.dumps(data, indent=4, default=default_converter)

# Guardar en un archivo
with open('output.json', 'w') as f:
    f.write(json_pretty)

# Imprimir el JSON bonito
print(json_pretty)

 
print( rpt_quotation_format(1816,'COT1816.pdf'))

#print(items)




