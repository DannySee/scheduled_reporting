import data_centers as db
from datetime import datetime

timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

sus = db.sus('240')
sql_server = db.sql_server()

agreements_created_yesterday = sus.execute(f'''
    SELECT DISTINCT 
    '' AS CUSTOMER_ID, 
    '' AS PROGRAM_ID, 
    '' AS USER_ID, 
    '' AS DAB, 
    '' AS CUSTOMER, 
    '' AS PROGRAM, 
    LEFT(RIGHT(M7VASD, 4),2) || '/' || RIGHT(M7VASD, 2) || '/' || LEFT(M7VASD,4) AS START_DATE, 
    LEFT(RIGHT(M7VASD, 4),2) || '/' || RIGHT(M7VASD, 2) || '/' || LEFT(M7VASD,4) AS END_DATE,
    CAST(M7VAGN AS VARCHAR(11)) AS LEAD_VA, 
    CAST(M7ACAN AS VARCHAR(11)) AS LEAD_CA, 
    M7AGTY AS VA_TYPE, 
    TRIM(M7VNBR) AS VENDOR, 
    M7COSP AS COST_BASIS, 
    NHAGTY AS CA_TYPE, 
    '' AS REBATE_BASIS, 
    TRIM(M7VPAN) AS PRE_APPROVAL, 
    TRIM(M7APNM) AS APPROP_NAME,
    '' AS CUSTOMER_ELIGIBILITY, 
    TRIM(DVPKGS) AS PACKET, 
    TRIM(DVPDDA) AS DISTRIBUTION_LIST, 
    '' AS COMMENTS, 
    TRIM(M7VAGD) AS SUS_DESCRIPTION, 
    CAST(M7EADT AS VARCHAR(11)) AS SUS_CREATE_DATE, 
    CAST(M7EATM AS VARCHAR(11)) AS SUS_CREATE_TIME, 
    M7EAID AS SUS_CREATE_ID, 
    '{timestamp}' AS TIMESTAMP

    FROM SCDBFP10.PMVHM7PF 

    INNER JOIN SCDBFP10.USCNAZPF
    ON RIGHT(CONCAT('000000000', M7VAGN),9) = AZCEEN
    AND TRIM(AZCEAI) = 'VA'

    LEFT JOIN SCDBFP10.PMDPDVRF
    ON M7VAGN = TRIM(DVCPM9)
    AND TRIM(DVCPTY) = 'VA'

    LEFT JOIN SCDBFP10.PMPVNHPF
    ON M7ACAN = NHCANO

    WHERE M7EADT = 20230616             
''').fetchall()

updates = {}

for row in agreements_created_yesterday[:5]:

    prior_va = sus.execute(f'''     
        SELECT MAX(CAST(IFNULL(M7VAGN,'') AS VARCHAR(11))) AS VA
                           
        FROM SCDBFP10.PMVHM7PF 
                    
        INNER JOIN (                  
            SELECT DISTINCT CAST(QBVAGN AS INT) AS VA
            FROM SCDBFP10.PMPZQBPF
            INNER JOIN (
                SELECT DISTINCT QBITEM AS ITEM, QBXVBS AS REBATE_BASIS
                FROM SCDBFP10.PMPZQBPF 
                WHERE TRIM(QBVAGN) = '{row.LEAD_VA}'
            )
            ON QBITEM = ITEM 
            AND QBXVBS = REBATE_BASIS
        ) AS ITEM
        ON M7VAGN = ITEM.VA

        INNER JOIN (
            SELECT DISTINCT AZCEEN AS VA
            FROM SCDBFP10.USCNAZPF 
            INNER JOIN (  
                SELECT AZPCIE AS IEA, AZPCSP AS SPEC
                FROM SCDBFP10.USCNAZPF 
                WHERE TRIM(AZCEEN) = RIGHT(CONCAT('000000000',{row.LEAD_VA}),9)
                AND TRIM(AZCEAI) = 'VA'
            ) 
            ON AZPCIE = IEA 
            AND AZPCSP = SPEC
        ) AS CUSTOMER
        ON RIGHT(CONCAT('000000000',M7VAGN),9) = CUSTOMER.VA
                    
        LEFT JOIN SCDBFP10.PMDPDVRF
        ON M7VAGN = TRIM(DVCPM9)
        AND TRIM(DVCPTY) = 'VA'

        WHERE M7VAGN < {row.LEAD_VA}
        AND M7VAGD NOT LIKE '%VOID%'
        AND TRIM(DVPDDA) = '{row.DISTRIBUTION_LIST}'
        AND M7COSP = '{row.COST_BASIS}'
    ''').fetchone()

    if prior_va is None:

        insert_value = ','.join(str(column) for column in row)
        print(insert_value)
        sql_server.execute(f'INSERT INTO hive_programs VALUES{insert_value}')

        print(f'inserted {row.LEAD_VA}')

    else:
        
        prior_record = sql_server.execute(f"SELECT CUSTOMER_ID, PROGRAM_ID, USER_ID, CUSTOMER, PROGRAM FROM hive_programs WHERE LEAD_VA = '{prior_va.VA}'").fetchone()
        
        sql_server.execute(f'''
            UPDATE hive_programs
            SET 
                START_DATE = '{row.START_DATE}',
                END_DATE = '{row.END_DATE}',
                LEAD_VA = '{row.LEAD_VA}',
                LEAD_CA = '{row.LEAD_CA}',
                VA_TYPE = '{row.VA_TYPE}',
                VENDOR = '{row.VENDOR}',
                COST_BASIS = '{row.COST_BASIS}',
                CA_TYPE = '{row.CA_TYPE}',
                REBATE_BASIS = '{row.REBATE_BASIS}',
                PRE_APPROVAL = '{row.PRE_APPROVAL}',
                APPROP_NAME = '{row.APPROP_NAME}',
                CUSTOMER_ELIGIBILITY = '{row.CUSTOMER_ELIGIBILITY}',
                PACKET = '{row.PACKET}',
                DISTRIBUTION_LIST = '{row.DISTRIBUTION_LIST}',
                SUS_DESCRIPTION = '{row.SUS_DESCRIPTION}',
                SUS_CREATE_DATE = '{row.SUS_CREATE_DATE}',
                SUS_CREATE_TIME = '{row.SUS_CREATE_TIME}',
                TIMESTAMP = '{row.TIMESTAMP}'
            WHERE LEAD_VA = '{prior_va.VA}'
        ''')

        print(f'updated {row.LEAD_VA}')

sql_server.commit()