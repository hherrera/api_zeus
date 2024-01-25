
from typing import List
from helpers.db_supabase import supabase


def upsertProducts(product:dict):
    """Insert/update, debe incluir al key (id) """ 
    data, count = supabase.table('products').upsert(product).execute()

    return data[1]
