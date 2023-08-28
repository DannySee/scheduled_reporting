import date_formats as dt
import warnings
import pandas as pd

from data_pull import sus_reporting
from data_centers import sql_server

today = dt.pretty("today")


def import_alaska_agreements(cnn_sus, site):
    return


def export_alaska_agreements(filename):

    cnn_server = sql_server()

    with open('sql\\alaska_bot\\header.sql', 'r') as sql:
        sql_header = sql.read()
    with open('sql\\alaska_bot\\items.sql', 'r') as sql:
        sql_items = sql.read()
    with open('sql\\alaska_bot\\customers.sql', 'r') as sql:
        sql_customers = sql.read()
    with open('sql\\alaska_bot\\lapsed.sql', 'r') as sql:
        sql_lapsed = sql.read()

    tabs = {
        'Header': sql_header,
        'Items': sql_items,
        'Customers': sql_customers,
        'Lapsed': sql_lapsed
    }

    warnings.filterwarnings('ignore')
    
    with pd.ExcelWriter(filename) as writer:
        for sheet_name in tabs:
            df = pd.read_sql_query(tabs[sheet_name], cnn_server)
            df.to_excel(writer, sheet_name=sheet_name, index=False, freeze_panes=(1, 0))

    warnings.resetwarnings()

    cnn_server.close()


daily_validation = {
    'custom_job': {'import': import_alaska_agreements, 'export': export_alaska_agreements},
    'send_if_null': True,
    'filename': f'Alaska_Agreement_Validation_{today}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'Daily Alaska Agreement Validation {today}',
    'mail_body': f'Daily Alaska Agreement Validation:\nAgreement(s) created {dt.pretty("yesterday")}.'
} 