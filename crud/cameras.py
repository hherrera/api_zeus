from typing import List
from helpers.db_supabase import supabase


def fecthCamerabyId(camera_id:int):

  data, count = supabase.table('cameras').select('*').eq('id',camera_id ).execute()

  return data[1]


def fecthCamerabyDoorId(door_id:int):

  data, count = supabase.table('cameras').select('*').eq('door_id',door_id ).execute()

  return data[1]