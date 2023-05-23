import date_formats as dt
import pandas as pd
import sql
import warnings

from data_centers import sql_server

today = dt.pretty("today")

############################################################################################
# Foodbuy Overlap Reports
############################################################################################

def import_foodbuy_overlaps(cnn_sus, site):

    if site != '240':

        cnn_server = sql_server()

        overlaps = {
            'Foodbuy_Overlap_Header': sql.foodbuy_overlap_header_sus,
            'Foodbuy_Overlap_Item': sql.foodbuy_overlap_item_sus,
            'Foodbuy_Overlap_customer': sql.foodbuy_overlap_customer_sus
        }

        for table in overlaps:

            rows = cnn_sus.execute(overlaps[table]).fetchall()
            if len(rows) > 0:
                dataset = ','.join(str(row) for row in rows)
                cnn_server.execute(f"INSERT INTO {table} VALUES{dataset}")

            print(table)
                            
        cnn_server.execute(sql.foodbuy_server_cleanup)
        cnn_server.commit()
        cnn_server.close()


def export_foodbuy_overlaps(filename):

    cnn_server = sql_server()

    overlaps = {
        'Header': sql.foodbuy_overlap_header_server,
        'Item': sql.foodbuy_overlap_item_server,
        'Customer': sql.foodbuy_overlap_customer_server
    }

    warnings.filterwarnings('ignore')
    
    with pd.ExcelWriter(filename) as writer:
        for sheet_name in overlaps:
            df = pd.read_sql_query(overlaps[sheet_name], cnn_server)
            df.to_excel(writer, sheet_name=sheet_name, index=False, freeze_panes=(1, 0))

    warnings.resetwarnings()

    cnn_server.close()


foodbuy_overlaps = {
    'custom_job': {'import': import_foodbuy_overlaps, 'export': export_foodbuy_overlaps},
    'filename': f'Foodbuy_Overlapping_Deals_{today}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'Foodbuy Overlapping Deals Report: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Overlapping Foodbuy Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
} 

############################################################################################
# Daily rebate basis validation
############################################################################################

rebate_basis_validatoin = {
    'sql': sql.rebate_basis_validation, 
    'filename': f'Rebate_Basis_Validation_{today}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'Daily Rebate Basis Validation {today}',
    'mail_body': f'Deviated Agreements:\nDaily Rebate Basis Violation {today}.'
} 