
from typing import List
from helpers.db_supabase import supabase


def upsertInvoice(order:dict):
    """Insert/update, debe incluir al key (id) """ 
    data, count = supabase.table('invoices').upsert(order).execute()

    return data[1]

def upsertItemInvoice(item:dict):
    
    data, count = supabase.table('invoicesItems').upsert(item).execute()

    return data[1]

def fetchInvoicesbyStatus(status:List[str]):
    
    data, count = supabase.table('invoices').select('id').in_('status',status ).execute()

    return data[1]