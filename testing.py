from services.zOrders import getOrdersAll, getOrder, getOrderItems
from services.zDispatch import getDispatchAll, getDispatch
from commands.sync import sync_orders , sync_dispatch
from crud.orders import fetchOrdersbyStatus
import debugpy
# Habilita la depuración en el puerto 5679
debugpy.listen(('0.0.0.0', 5678))

#response = getOrdersAll(0)
#response = getDispatchAll(0)
#print(response)
#print(getDispatch(17196))


#order = getOrder(1016999)
#items= getOrderItems(1016999)

data = sync_dispatch(type='New')
print(data)

data = sync_orders(type='New')
print(data)

data =fetchOrdersbyStatus(['Pendiente','Parcialmente Satisfecho'])
print(data)
#print(int(data[0]['id']))


#print(order)




#print(items)




