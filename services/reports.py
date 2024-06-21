import pandas as pd
from settings import settings
from  services.gsheets import dataframe_to_google_sheets, dataframes_to_google_sheets

from datetime import datetime


from typing import List
from helpers.db_supabase import supabase

def fetch_trucks_control(date_ref,emails):
    try:
        # Suponiendo que 'get_trucks_control' es un Procedimiento Almacenado en Supabase
        data = supabase.rpc('get_trucks_control', {'fecha_ref': date_ref}).execute()
        
        # Convertir el resultado en una lista de diccionarios si se devuelve algún dato
        df = pd.DataFrame(data.data if data.data else [])
        
        # Verificar si el DataFrame está vacío
        if df.empty:
            raise ValueError("No se encontraron datos para la fecha proporcionada.")
        
        # Convertir la columna 'hora' a datetime y formatearla para mostrar solo horas y minutos
        df['hora'] = pd.to_datetime(df['hora']).dt.strftime('%H:%M')
        
        # Generar el título de la hoja con la fecha y hora actual
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        sheet_title = f'Reporte control camiones {now}'
        
        # Llamar a la función y capturar la URL de la hoja de Google Sheets
        sheet_url = dataframe_to_google_sheets(df, emails, sheet_title, settings.SERVICE_ACCOUNT)
        
        # Asegurarse de que la URL de la hoja de Google Sheets se haya obtenido correctamente
        if not sheet_url:
            raise ValueError("No se pudo obtener la URL de la hoja de Google Sheets.")
        
        return [{"success": True, "sheet_url": sheet_url}]
    
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante el proceso
        print(f"Error al generar el reporte control vehicular: {e}")
        return [{"success": False, "error": str(e)}]


def fetch_vehicle_control(date_ref,emails):
    try:
        # Suponiendo que 'get_trucks_control' es un Procedimiento Almacenado en Supabase
        data = supabase.rpc('get_vehicle_control', {'fecha_ref': date_ref}).execute()
        
        # Convertir el resultado en una lista de diccionarios si se devuelve algún dato
        df = pd.DataFrame(data.data if data.data else [])
        
        # Verificar si el DataFrame está vacío
        if df.empty:
            raise ValueError("No se encontraron datos para la fecha proporcionada.")
        
        # Convertir la columna 'hora' a datetime y formatearla para mostrar solo horas y minutos
        df['hora'] = pd.to_datetime(df['hora']).dt.strftime('%H:%M')
        
        # Generar el título de la hoja con la fecha y hora actual
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        sheet_title = f'Reporte control vehicular [{date_ref}] {now}'
        
        # Llamar a la función y capturar la URL de la hoja de Google Sheets
        sheet_url = dataframe_to_google_sheets(df, emails, sheet_title, settings.SERVICE_ACCOUNT)
        
        # Asegurarse de que la URL de la hoja de Google Sheets se haya obtenido correctamente
        if not sheet_url:
            raise ValueError("No se pudo obtener la URL de la hoja de Google Sheets.")
        
        return [{"success": True, "sheet_url": sheet_url}]
    
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante el proceso
        print(f"Error al generar el reporte control vehicular: {e}")
        return [{"success": False, "error": str(e)}]



#get_order_information

def fetch_order_information(date_ref,emails):
    try:
        # Suponiendo que 'get_trucks_control' es un Procedimiento Almacenado en Supabase
        data = supabase.rpc('get_order_information', {'date_ref': date_ref}).execute()
        
        # Convertir el resultado en una lista de diccionarios si se devuelve algún dato
        df = pd.DataFrame(data.data if data.data else [])
        
        # Verificar si el DataFrame está vacío
        if df.empty:
            raise ValueError("No se encontraron datos para la fecha proporcionada.")
        
        #get_active_company_vehicles()
        vehicles = supabase.rpc('get_active_company_vehicles').execute()
        
        df_v = pd.DataFrame(vehicles.data if vehicles.data else [])
        print(df_v)
        print(df)
        # adicionar aca 
        # Asegurar que 'plate' existe en ambos DataFrames
        if 'placa' in df.columns and 'plate' in df_v.columns:
            # Filtrar los valores de 'plate' en df_v que no están en 'placa' de df
            unique_plates = df_v[~df_v['plate'].isin(df['placa'])]
            
            # Crear un DataFrame vacío con las mismas columnas que df
            new_rows = pd.DataFrame(columns=df.columns)
            
            # Asignar los valores únicos de 'plate' de df_v a la columna 'placa' en new_rows
            new_rows['placa'] = unique_plates['plate']
            
            # Concatenar new_rows al final de df
            df = pd.concat([df, new_rows], ignore_index=True)
        # Generar el título de la hoja con la fecha y hora actual
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        sheet_title = f'Reporte de programacion diaria [{date_ref}] {now}'
        
        # Llamar a la función y capturar la URL de la hoja de Google Sheets
        sheet_url = dataframe_to_google_sheets(df, emails, sheet_title, settings.SERVICE_ACCOUNT)
        
        # Asegurarse de que la URL de la hoja de Google Sheets se haya obtenido correctamente
        if not sheet_url:
            raise ValueError("No se pudo obtener la URL de la hoja de Google Sheets.")
        
        return [{"success": True, "sheet_url": sheet_url}]
    
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante el proceso
        print(f"Error al generar el informe de distribuidores : {e}")
        return [{"success": False, "error": str(e)}]



#report_loading_distribution

def fetch_loading_distribution(date_ref,emails):
    try:
        # Suponiendo que 'get_trucks_control' es un Procedimiento Almacenado en Supabase
        data = supabase.rpc('report_loading_distribution', {'date_ref': date_ref}).execute()
        
        # Convertir el resultado en una lista de diccionarios si se devuelve algún dato
        df = pd.DataFrame(data.data if data.data else [])
        
        # Verificar si el DataFrame está vacío
        if df.empty:
            raise ValueError("No se encontraron datos para la fecha proporcionada.")
        # Verificar si hay valores NA antes de la conversión y llenar con un valor predeterminado o eliminar
        if df[['hora_entrada', 'hora_entrega_orden', 'hora_cargue', 'hora_conteo', 'hora_salida']].isnull().any().any():
            print("Hay valores nulos en las columnas de fecha/hora.")
            # Puedes optar por llenar los valores nulos con una fecha/hora específica o eliminar esas filas
            df.dropna(subset=['hora_entrada', 'hora_entrega_orden', 'hora_cargue', 'hora_conteo', 'hora_salida'], inplace=True)
            # O puedes llenar los valores NA con una fecha/hora que tenga sentido en tu contexto
            # df.fillna({'hora_entrada': fecha_hora_predeterminada, 'hora_entrega_orden': fecha_hora_predeterminada, ...}, inplace=True)

                # Convertir la columna 'hora' a datetime y formatearla para mostrar solo horas y minutos
        #print(df['tiempo_espera']) = df['hora_entrada']- df['hora_entrega_orden']
        df['hora_entrega_orden'] = pd.to_datetime(df['hora_entrega_orden'])
        df['hora_entrada'] = pd.to_datetime(df['hora_entrada'])
        df['hora_cargue'] = pd.to_datetime(df['hora_cargue'])
        df['hora_conteo'] = pd.to_datetime(df['hora_conteo'])
        df['hora_salida'] = pd.to_datetime(df['hora_salida'])
        
        
        df['tiempo_espera'] = ((df['hora_entrada'] - df['hora_entrega_orden']).dt.total_seconds() / 60).astype(int)
        df['tiempo_carque'] = ((df['hora_cargue'] - df['hora_entrada']).dt.total_seconds() / 60).astype(int)
        df['tiempo_conteo'] = ((df['hora_conteo'] - df['hora_cargue']).dt.total_seconds() / 60).astype(int)
        df['tiempo_salida'] = ((df['hora_salida'] - df['hora_conteo']).dt.total_seconds() / 60).astype(int)




        # Generar el título de la hoja con la fecha y hora actual
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        sheet_title = f'Informe de distribuidores [{date_ref}] - {now}'
        
        # Llamar a la función y capturar la URL de la hoja de Google Sheets
        sheet_url = dataframe_to_google_sheets(df, emails, sheet_title, settings.SERVICE_ACCOUNT)
        
        # Asegurarse de que la URL de la hoja de Google Sheets se haya obtenido correctamente
        if not sheet_url:
            raise ValueError("No se pudo obtener la URL de la hoja de Google Sheets.")
        
        return [{"success": True, "sheet_url": sheet_url}]
    
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante el proceso
        print(f"Error al generar el informe de distribuidores : {e}")
        return [{"success": False, "error": str(e)}]

def fetch_loading_distribution_interval(start_date:str,end_date:str,emails:List[str]):
    try:
        # Suponiendo que 'get_trucks_control' es un Procedimiento Almacenado en Supabase
        data = supabase.rpc('report_loading_distribution_interval', {'start_date': start_date,'end_date': end_date}).execute()
        
        # Convertir el resultado en una lista de diccionarios si se devuelve algún dato
        df = pd.DataFrame(data.data if data.data else [])
        
        # Verificar si el DataFrame está vacío
        if df.empty:
            raise ValueError("No se encontraron datos para la fecha proporcionada.")
        # Verificar si hay valores NA antes de la conversión y llenar con un valor predeterminado o eliminar
        if df[['hora_entrada', 'hora_entrega_orden', 'hora_cargue', 'hora_conteo', 'hora_salida']].isnull().any().any():
            print("Hay valores nulos en las columnas de fecha/hora.")
            # Puedes optar por llenar los valores nulos con una fecha/hora específica o eliminar esas filas
            df.dropna(subset=['hora_entrada', 'hora_entrega_orden', 'hora_cargue', 'hora_conteo', 'hora_salida'], inplace=True)
            # O puedes llenar los valores NA con una fecha/hora que tenga sentido en tu contexto
            # df.fillna({'hora_entrada': fecha_hora_predeterminada, 'hora_entrega_orden': fecha_hora_predeterminada, ...}, inplace=True)

                # Convertir la columna 'hora' a datetime y formatearla para mostrar solo horas y minutos
        #print(df['tiempo_espera']) = df['hora_entrada']- df['hora_entrega_orden']
        df['hora_entrega_orden'] = pd.to_datetime(df['hora_entrega_orden'])
        df['hora_entrada'] = pd.to_datetime(df['hora_entrada'])
        df['hora_cargue'] = pd.to_datetime(df['hora_cargue'])
        df['hora_conteo'] = pd.to_datetime(df['hora_conteo'])
        df['hora_salida'] = pd.to_datetime(df['hora_salida'])
        
        
        df['tiempo_espera'] = ((df['hora_entrada'] - df['hora_entrega_orden']).dt.total_seconds() / 60).astype(int)
        df['tiempo_carque'] = ((df['hora_cargue'] - df['hora_entrada']).dt.total_seconds() / 60).astype(int)
        df['tiempo_conteo'] = ((df['hora_conteo'] - df['hora_cargue']).dt.total_seconds() / 60).astype(int)
        df['tiempo_salida'] = ((df['hora_salida'] - df['hora_conteo']).dt.total_seconds() / 60).astype(int)




        # Generar el título de la hoja con la fecha y hora actual
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        sheet_title = f'Informe de distribuidores [ {start_date} - {end_date} ] - {now}'
        
        # Llamar a la función y capturar la URL de la hoja de Google Sheets
        sheet_url = dataframe_to_google_sheets(df, emails, sheet_title, settings.SERVICE_ACCOUNT)
        
        # Asegurarse de que la URL de la hoja de Google Sheets se haya obtenido correctamente
        if not sheet_url:
            raise ValueError("No se pudo obtener la URL de la hoja de Google Sheets.")
        
        return [{"success": True, "sheet_url": sheet_url}]
    
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante el proceso
        print(f"Error al generar el informe de distribuidores por rando de fechas : {e}")
        return [{"success": False, "error": str(e)}]



#load_report_driver_by_month
#load_report_by_month_and_year
def fetch_load_report_driver_by_month(year:int, month:int,emails):
    try:
        # Suponiendo que 'load_report_by_month_and_year' es un Procedimiento Almacenado en Supabase
        data = supabase.rpc('load_report_by_month_and_year', {'year_ref': year,'month_ref':month}).execute()
        print(data)
        # Convertir el resultado en una lista de diccionarios si se devuelve algún dato
        df = pd.DataFrame(data.data if data.data else [])
        # Verificar si el DataFrame está vacío
        if df.empty:
            raise ValueError("No se encontraron datos para la fecha proporcionada.")
        
        # Suponiendo que 'load_report_by_month_and_year' es un Procedimiento Almacenado en Supabase
        data = supabase.rpc('load_report_driver_by_month', {'year_ref': year,'month_ref':month}).execute()
        print(data)
        # Convertir el resultado en una lista de diccionarios si se devuelve algún dato
        df2 = pd.DataFrame(data.data if data.data else [])
        # Verificar si el DataFrame está vacío
        if df2.empty:
            raise ValueError("No se encontraron datos para la fecha proporcionada.")
        
        dfs = []
        # Convertir la columna 'hora' a datetime y formatearla para mostrar solo horas y minutos
        #print(df['tiempo_espera']) = df['hora_entrada']- df['hora_entrega_orden']
        dfs.append(df2)
        dfs.append(df)


        # Generar el título de la hoja con la fecha y hora actual
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        sheet_title = f'Informe incentivos conductores [{year}-{month}]'
        
        # Llamar a la función y capturar la URL de la hoja de Google Sheets
        sheet_url = dataframes_to_google_sheets(dfs, emails, sheet_title, settings.SERVICE_ACCOUNT)
        
        # Asegurarse de que la URL de la hoja de Google Sheets se haya obtenido correctamente
        if not sheet_url:
            raise ValueError("No se pudo obtener la URL de la hoja de Google Sheets.")
        
        return [{"success": True, "sheet_url": sheet_url}]
    
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante el proceso
        print(f"Error al generar el Informe incentivos conductores : {e}")
        return [{"success": False, "error": str(e)}]