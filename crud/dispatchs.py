
from typing import List
from helpers.db_supabase import supabase


def upsertDispatch(dispatch:dict):
    """Insert/update, debe incluir al key (id) """ 
    data, count = supabase.table('dispatchs').upsert(dispatch).execute()

    return data[1]

def upsertItemDispatch(item:dict):
    
    data, count = supabase.table('dispatchsItems').upsert(item).execute()

    return data[1]

def fetchDispatchbyStatus(status:List[str]):
    
    data, count = supabase.table('dispatchs').select('id').in_('status',status ).execute()

    return data[1]

def deleteDispatchsOrders(dispacth_id:int):
    
    data, count = supabase.table('dispatchs_orders').delete().eq('dispatch_id',dispacth_id).execute()

    return data[1]

def insertDispatchsOrders(item:dict):
    
    data, count = supabase.table('dispatchs_orders').insert(item).execute()

    return data[1]