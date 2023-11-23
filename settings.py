import os
from typing import Any
import pyodbc

class Settings:
    def __init__(self):
       
        ## load variables of .env
        
        self.PROJECT_NAME:str = "API gateway from ZEUS"
        self.PROJECT_VERSION:str = "0.0.1"

        ##
        self.SERVER:str = os.environ.get("SERVER")
        self.USER:str = os.environ.get("USER")
        self.PASSWORD:str = os.environ.get("PASSWORD")
        self.PORT:str = os.environ.get("PORT")
        self.DATABASE:str = os.environ.get("DATABASE")
        self.DB_INVENTARIO:str = os.environ.get("DB_INVENTARIO")
        self.DB_NOMINA:str = os.environ.get("DB_NOMINA")
        self.DB_CONTABILIDAD:str = os.environ.get("DB_CONTABILIDAD")
        
        self.DRIVER:str = os.environ.get("DRIVER")

        ## Supabase 
        self.SUPABASE_URL=os.environ.get("SUPABASE_URL")
        self.SUPABASE_KEY=os.environ.get("SUPABASE_KEY")

    def database_url(self):
       return  f"Driver={self.DRIVER};Server={self.SERVER};PORT={self.PORT};DATABASE={self.DATABASE};UID={self.USER};pwd={self.PASSWORD};TDS_Version=7.2;CHARSET=UTF-8;"
    def set_database(self,dbname:str):
        self.DATABASE:str=dbname

settings = Settings()