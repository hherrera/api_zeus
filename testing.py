from services.zOrders import getOrdersAll, getOrder, getOrderItems
from services.zDispatch import getDispatchAll, getDispatch
from commands.sync import sync_orders , sync_dispatch, sync_products
from crud.orders import fetchOrdersbyStatus
from crud.cameras import fecthCamerabyId
import debugpy
# Habilita la depuración en el puerto 5679
debugpy.listen(('0.0.0.0', 5678))

#response = getOrdersAll(0)
#response = getDispatchAll(0)
#print(response)
#print(getDispatch(17196))


#order = getOrder(1016999)
#items= getOrderItems(1016999)

## una vez al dia - sincronizar desde la app 
#sync_products()

from fastapi import FastAPI, HTTPException
import asyncpg
import asyncio

app = FastAPI()
async def get_db_connection():
    # Replace with your database credentials
    return await asyncpg.connect(user='user', password='password', database='db', host='127.0.0.1')
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    conn = await get_db_connection()
    try:
        # Be careful with raw SQL to avoid SQL injection
        row = await conn.fetchrow('SELECT * FROM items WHERE id = $1', item_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return dict(row)
    finally:
        await conn.close()


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




#print(items)




