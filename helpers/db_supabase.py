import os

from supabase import create_client, Client
from settings import settings
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

