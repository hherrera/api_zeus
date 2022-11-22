import os
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
        self.DRIVER:str = os.environ.get("DRIVER")
       
    def database_url(self):
       return  f"Driver={self.DRIVER};Server={self.SERVER};PORT={self.PORT};DATABASE={self.DATABASE};UID={self.USER};pwd={self.PASSWORD};TDS_Version=7.2;CHARSET=UTF-8;"
   
settings = Settings()