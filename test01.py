import pandas as pd
from settings import settings
from  services.gsheets import dataframe_to_google_sheets
from services.reports import fetch_trucks_control, fetch_load_report_driver_by_month,fetch_loading_distribution, fetch_order_information
from datetime import datetime
from services.zDocsRelations import getOrdersRelations
from services.zClients import getCreditLimitForClient, getAccountBalanceForClient
date_ref = '2024-04-04'

#list_trucks_control = fetch_loading_distribution(date_ref=date_ref,emails=["hherrera@araujoysegovia.com"])

#list_trucks_control = fetch_load_report_driver_by_month(2024,3 ,["hherrera@araujoysegovia.com"])
#print(getOrdersRelations(104835))

#print(list_trucks_control)
print(getCreditLimitForClient(client_id='901120547'))
print(getAccountBalanceForClient(client_id='901120547',code='28050501'))
