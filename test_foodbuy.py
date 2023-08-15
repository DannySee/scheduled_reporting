
import deviated_agreements as dpm
import data_centers as cnn

from excel import create_file
from data_pull import sus_reporting


def pull_from_sus():
    sus_reporting([dpm.foodbuy_overlaps],cnn.all_sites)


def deliver_report():

    sql_server = cnn.sql_server()
    cur = sql_server.cursor()

    query = """
        
        SELECT TOP 1000000
        T1.SITE_NBR AS SITE,
        T1.SITE_NAME AS SITE_NAME, 
        'VA' AS AGREEMENT_TYPE, 
        '' AS TERM_SET_CODE, 
        '' AS TERM_SET_NAME, 
        T1.FOODBUY_AGREEMENT,
        T1.FOODBUY_DESCRIPTION,
        T1.FOODBUY_START, 
        T1.FOODBUY_END,
        T1.DIRECT_AGREEMENT,
        T1.DIRECT_START, 
        T1.DIRECT_END,
        T1.DCN, 
        T1.CUSTOMER_NAME,
        T2.ITEM,
        T2.ITEM_DESCRIPTION,
        'NATIONAL' AS LOCAL_NATIONAL,
        'MFR' AS SYSCO_MFR_OVR,
        T3.APPLIED_PRICING


        FROM Foodbuy_Overlap_Customer AS T1

        INNER JOIN FOODBUY_OVERLAP_ITEM AS T2
        ON T1.FOODBUY_AGREEMENT = T2.FOODBUY_AGREEMENT
        AND T1.DIRECT_AGREEMENT = T2.DIRECT_AGREEMENT

        INNER JOIN FOODBUY_OVERLAP_HEADER AS T3
        ON T1.FOODBUY_AGREEMENT = T3.FOODBUY_AGREEMENT
        AND T1.DIRECT_AGREEMENT = T3.DIRECT_AGREEMENT

        ORDER BY T1.FOODBUY_AGREEMENT, T1.DIRECT_AGREEMENT, T1.DCN, T2.ITEM


    """

    # fetch data from system
    cur.execute(query)
    query_results = cur.fetchall()

    filename = f"C:\\Temp\\outgoing_mail\\foodbuy_test2.xlsx"
    headers = [desc[0] for desc in cur.description]
    content = [list(map(str, row)) for row in query_results]

    print(headers)
    
    create_file(filename, headers, content)


deliver_report()