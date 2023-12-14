
from typing import List
from helpers.db_supabase import supabase


def upsertOrder(order:dict):
    """Insert/update, debe incluir al key (id) """ 
    data, count = supabase.table('orders').upsert(order).execute()

    return data[1]

def upsertItemOrder(item:dict):
    
    data, count = supabase.table('ordersItems').upsert(item).execute()

    return data[1]

def fetchOrdersbyStatus(status:List[str]):
    
    data, count = supabase.table('orders').select('*').in_('status',status ).execute()

    return data[1]