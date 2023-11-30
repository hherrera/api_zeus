from helpers.db_supabase import supabase


def select(name:str):
    """select parameters """ 
    data,count = supabase.table('parameters').select("*").eq("name", name).execute()

    return data[1]

def update(name:str, value:str):
    data,count = supabase.table('parameters').update({'value':value}).eq('name', name).execute()

    return data[1]