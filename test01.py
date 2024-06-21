import pandas as pd
from settings import settings
from  services.gsheets import dataframe_to_google_sheets
from services.reports import fetch_trucks_control,fetch_loading_distribution_interval,fetch_vehicle_control,fetch_load_report_driver_by_month,fetch_loading_distribution, fetch_order_information
from datetime import datetime
from services.zDocsRelations import getOrdersRelations
from services.zClients import getCreditLimitForClient, getAccountBalanceForClient
from crud.orders import deleteItemsOrder
start_date = '2024-06-20'
end_date= '2024-06-20'


#print(deleteItemsOrder(105743,emails=["hherrera@araujoysegovia.com"])
list_trucks_control = fetch_loading_distribution_interval(start_date=start_date,end_date=end_date,emails=["hherrera@araujoysegovia.com"])
print(list_trucks_control)


#result = fetch_vehicle_control(date_ref,emails=["hherrera@araujoysegovia.com"])
#list_trucks_control = fetch_loading_distribution(date_ref=date_ref,emails=["hherrera@araujoysegovia.com"])
#print(result)
#list_trucks_control = fetch_load_report_driver_by_month(2024,3 ,["hherrera@araujoysegovia.com"])
#print(getOrdersRelations(104835))

#print(list_trucks_control)
#print(getCreditLimitForClient(client_id='901120547'))
#print(getAccountBalanceForClient(client_id='901120547',code='28050501'))
#print(list_trucks_control)

