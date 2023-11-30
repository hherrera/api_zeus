
from typing import List
from helpers.db_supabase import supabase


def upsertDispatch(dispatch:dict):
    """Insert/update, debe incluir al key (id) """ 
    data, count = supabase.table('dispatchs').upsert(dispatch).execute()

    return data[1]

def upsertItemDispatch(item:dict):
    
    data, count = supabase.table('dispatchItems').upsert(item).execute()

    return data[1]