
from typing import List
from helpers.db_supabase import supabase


def upsertOrder(order:dict):
    """Insert/update, debe incluir al key (id) """ 
    data, count = supabase.table('orders').upsert(order).execute()

    return data[1]

#data.extend(data1)
def upsertOrderDocRelations(order_doc_relations:dict):
    """Insert/update, debe incluir al key (id) """ 
    data, count = supabase.table('orders_doc_relations').upsert(order_doc_relations).execute()

    return data[1]

def upsertItemOrder(item:dict):
    
    if item:
     data, count = supabase.table('ordersItems').upsert(item).execute()
     return data[1]
    return []

def deleteItemsOrder(order_id:int):
    
    data, count = data, count = supabase.table('ordersItems').delete().eq('order_id', order_id).execute()

    return data[1]

def fetchOrdersbyStatus(status:List[str]):
    
    data, count = supabase.table('orders').select('id').in_('status',status ).execute()

    return data[1]