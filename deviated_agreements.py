import date_formats as dt
import sql

from data_centers import sql_server


def import_foodbuy_overlaps(cnn_sus):

    cnn_server = sql_server()

    overlaps = {
        'Foodbuy_Overlap_Header': sql.overlap_header_sus,
        'Foodbuy_Overlap_Item': sql.overlap_item_sus,
        'Foodbuy_Overlap_customer': sql.overlap_customer_sus
    }

    for table in overlaps:

        rows = cnn_sus.execute(overlaps[table]).fetchall()
        dataset = ','.join(str(row) for row in rows)
        cnn_server.execute(f"INSERT INTO {table} VALUES{dataset}")

                        
    cnn_server.execute(sql.server_cleanup)
    cnn_server.commit()
    cnn_server.close()


def export_foodbuy_overlaps(filename):

    return


foodbuy_overlaps = {
    'custom_job': {'import': import_foodbuy_overlaps, 'export': export_foodbuy_overlaps},
    'filename': f'Foodbuy_Overlapping_Deals_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'Foodbuy Overlapping Deals Report: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping Admin Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
} 


