import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from settings import settings

def dataframe_to_google_sheets(df: pd.DataFrame, email_shares: list[str], sheet_title: str, credentials_json: str) -> str:
    """
    Crea una hoja de cálculo en Google Sheets con los datos de un DataFrame
    y comparte la hoja de cálculo con una lista de emails. Retorna la URL de la hoja de cálculo compartida.

    Parámetros:
    df (pd.DataFrame): DataFrame a exportar.
    email_shares (list[str]): Lista de emails con los que compartir la hoja de cálculo.
    sheet_title (str): Título de la hoja de cálculo.
    credentials_json (str): Ruta al archivo JSON de las credenciales de la cuenta de servicio.

    Retorna:
    str: URL de la hoja de cálculo compartida.
    """
    # Definir el alcance y autenticar usando las credenciales
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(creds)

    # Crear una nueva hoja de cálculo con el título proporcionado
    sheet = client.create(sheet_title)
    
    # Compartir la hoja de cálculo con los emails especificados
    for email in email_shares:
        sheet.share(email, perm_type='user', role='writer')

    # Obtener la primera hoja de la hoja de cálculo
    worksheet = sheet.get_worksheet(0)
    print(f'Total registros DF:{len(df)} \n')
     # Ajustar el tamaño de la hoja de cálculo según el número de registros del DataFrame
    worksheet.resize(rows=len(df) + 1, cols=len(df.columns))
    # Actualizar la hoja de cálculo con los datos del DataFrame
    set_with_dataframe(worksheet, df)  # Utilizando gspread_dataframe para simplificar la actualización

    #print(f"Hoja de cálculo '{sheet_title}' creada y compartida con {', '.join(email_shares)}.")
    
    # Retornar la URL de la hoja de cálculo
    return sheet.url

def dataframes_to_google_sheets(dfs: list[pd.DataFrame], email_shares: list[str], sheet_title: str, credentials_json: str) -> str:
    """
    Crea una hoja de cálculo en Google Sheets con los datos de una lista de DataFrames
    y comparte la hoja de cálculo con una lista de emails. Cada DataFrame se coloca en una worksheet distinta.
    Retorna la URL de la hoja de cálculo compartida.

    Parámetros:
    dfs (list[pd.DataFrame]): Lista de DataFrames a exportar.
    email_shares (list[str]): Lista de emails con los que compartir la hoja de cálculo.
    sheet_title (str): Título de la hoja de cálculo.
    credentials_json (str): Ruta al archivo JSON de las credenciales de la cuenta de servicio.

    Retorna:
    str: URL de la hoja de cálculo compartida.
    """
    # Definir el alcance y autenticar usando las credenciales
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(creds)

    # Crear una nueva hoja de cálculo con el título proporcionado
    sheet = client.create(sheet_title)
    
    # Compartir la hoja de cálculo con los emails especificados
    for email in email_shares:
        sheet.share(email, perm_type='user', role='writer')

    # Por cada DataFrame en la lista, crear y actualizar una worksheet nueva
    for i, df in enumerate(dfs):
        # Título para cada worksheet basado en su índice
        worksheet_title = f'Hoja {i+1}'
        
        # Crear una nueva worksheet con el título
        if i == 0:
            worksheet = sheet.get_worksheet(0)
            worksheet.update_title(worksheet_title)
        else:
            worksheet = sheet.add_worksheet(title=worksheet_title, rows="100", cols="20")
        
        # Actualizar la worksheet con los datos del DataFrame
        set_with_dataframe(worksheet, df)

    # Retornar la URL de la hoja de cálculo
    return sheet.url

