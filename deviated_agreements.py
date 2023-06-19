import date_formats as dt
import pandas as pd
import sql
import warnings

from data_centers import sql_server

today = dt.pretty("today")

############################################################################################
# Foodbuy Overlap Reports
############################################################################################
def insert_into_sql_server(cnn, dataset, table):
    
    # get row count of dataset
    row_count = len(dataset)

    # sql server has an insert row max of 1000 records - handle differently depending on size of dataset
    if row_count > 1000:

        # loop through dataset in chuncks of 1000 records
        for i in range(0, row_count, 1000):

            # format chunk of 1000 insert into sql server
            rows = ','.join(str(row) for row in dataset[i:i+1000])
            cnn.execute(f'INSERT INTO {table} VALUES{rows}')
            print(f'chunk upload {i} complete')
            
        # commit insert statement after all chunks have been loaded in the server
        cnn.commit()
    elif row_count > 0:

        # format dataset, insert into sql server and commit
        rows = ','.join(str(row) for row in dataset)
        cnn.execute(f'INSERT INTO {table} VALUES{rows}')
        cnn.commit()


def import_foodbuy_overlaps(cnn_sus, site):

    if site != '240':

        cnn_server = sql_server()

        overlaps = {
            'Foodbuy_Overlap_Header': [],
            'Foodbuy_Overlap_Item': [],
            'Foodbuy_Overlap_customer': []
        }

        overlaps['Foodbuy_Overlap_Header'] = cnn_sus.execute(sql.foodbuy_overlap_header_sus).fetchall()
        foodbuy_agreements = ",".join(str(row.FOODBUY_AGREEMENT) for row in overlaps['Foodbuy_Overlap_Header'])
        direct_agreements = ",".join(str(row.DIRECT_AGREEMENT) for row in overlaps['Foodbuy_Overlap_Header'])

        overlaps['Foodbuy_Overlap_Item'] = cnn_sus.execute(sql.foodbuy_overlap_item_sus(foodbuy_agreements, direct_agreements)).fetchall()
        overlaps['Foodbuy_Overlap_customer'] = cnn_sus.execute(sql.foodbuy_overlap_customer_sus(foodbuy_agreements, direct_agreements)).fetchall()

        for table in overlaps:
            print(f'processing {table}')
            insert_into_sql_server(cnn_server, overlaps[table], table)
            print(f'upload complete: {table}')
                            
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
    'send_if_null': True,
    'filename': f'Foodbuy_Overlapping_Deals_{today}',
    'data': [], 
    'headers': '',
    'mail_to': 'GPOCommercialDesk@Sysco.com',
    'mail_subject': f'Foodbuy Overlapping Deals Report: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Overlapping Foodbuy Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
} 

############################################################################################
# Daily rebate basis validation
############################################################################################

rebate_basis_validatoin = {
    'sql': sql.rebate_basis_validation, 
    'send_if_null': True,
    'filename': f'Rebate_Basis_Validation_{today}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com;duana.stewart@sysco.com',
    'mail_subject': f'Daily Rebate Basis Validation {today}',
    'mail_body': f'Deviated Agreements:\nDaily Rebate Basis Violation {today}.'
} 