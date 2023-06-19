import date_formats as dt

today = dt.sus('today')
yesterday = dt.sus('yesterday')
bolw = dt.sus('beginning_of_last_week')
eolw = dt.sus('end_of_last_week')
bom = dt.sus('beginning_of_month')
eom = dt.sus('end_of_month')
last_month = dt.pretty('month_back')
timestamp = dt.pretty('today')

############################################################################################
# Customer Incentives Queries
############################################################################################

daily_ci_validation = (f'''
    SELECT DISTINCT
    NHARCO AS SITE,
    '*MARKET*' AS MARKET,
    NHCANO AS CA,
    TRIM(NHCADC) AS DESCRIPTION,
    NHAGTY AS CA_TYPE,
    NHAPTY AS APP_TYPE,
    NHCASD AS START_DT,
    NHCAED AS END_DT,
    NHPFUM AS DROP_UNIT,
    NHPFDB AS DROP_BASIS,
    NHPFPD AS PERF_PERIOD,
    NHPFRB AS REBATE_BASIS,
    O5PFTR AS IN_DROP_QTY,
    O5TWKS AS TOTAL_SALES$,
    O5PFRA AS REBATE_AMT,
    AZPCIE AS IEA,
    AZPCSC AS SPEC_CD,
    TRIM(AZPCSP) AS CUSTOMER_SPEC, 
    CASE 
        WHEN NHPFRB = 'PC' AND O5PFRA > 3 THEN 'PC > 3%' 
        WHEN NHPFRB = 'DC' AND O5PFRA > 5 THEN 'DC > $5'
        WHEN NHPFRB = 'DP' AND O5PFRA > 0.25 THEN 'DP > $0.25'
        WHEN NHPFRB = 'DD' AND O5PFRA > 50 THEN 'DD > $50'
        WHEN O5PFTR < 0.001 THEN 'DROP QTY'
        ELSE '' 
    END AS ERROR

    FROM SCDBFP10.PMPVNHPF

    INNER JOIN SCDBFP10.PMPZO5L0 AS T2
    ON NHCANO = O5CANO

    LEFT JOIN SCDBFP10.USCNAZPF
    ON RIGHT('000000' || NHCANO, 9) = AZCEEN
    AND AZCEAI <> 'VA '

    WHERE (NHEADT = {yesterday}
    OR NHAPDT = {yesterday})
    AND NHAGRN = 0
    AND NHPPAF = 'PF'
''')

updl_violation = (f'''
    SELECT
    TRIM(NHARCO) AS SITE,
    '*MARKET*' AS MARKET,
    NHCANO AS CA,
    TRIM(NHCADC) AS DESCRIPTION,
    NHCASD AS START_DT,
    NHCAED AS END_DT,
    NHPFRB AS REBATE_BASIS

    FROM SCDBFP10.PMPVNHPF

    INNER JOIN SCDBFP10.PMPZO5L0 AS T2
    ON NHCANO = O5CANO

    WHERE NHCAED >= {today}
    AND NHAGTY = 'UPDL' 
    AND NHPFRB <> 'DL'
    AND NHAGRN = 0   
''')

customer_incentives_overlaps = (f'''
    SELECT DISTINCT
    TRIM(T1.NHARCO) AS SITE, 
    '*MARKET*' AS MARKET,
    T1.NHAGRN AS PRNT_LEAD_CA,
    T1.NHCANO AS PRNT_LOCAL_CA, 
    TRIM(T1.NHCADC) AS PRNT_DESCRIPTION,
    T1.NHAGTY AS PRNT_TYPE,
    T1.NHCASD AS PRNT_START, 
    T1.NHCAED AS PRNT_END,
    T2.NHAGRN AS CHLD_LEAD_CA,
    T2.NHCANO AS CHLD_LOCAL_CA, 
    TRIM(T2.NHCADC) AS CHLD_DESCRIPTION,
    T2.NHAGTY AS CHLD_TYPE,
    T2.NHCASD AS CHLD_START, 
    T2.NHCAED AS CHLD_END

    FROM SCDBFP10.PMPVNHPF AS T1 

    INNER JOIN SCDBFP10.PMPVNHPF AS T2
    ON T1.NHCADC = T2.NHCADC 
    AND T1.NHCAED >= T2.NHCASD
    AND T1.NHCASD <= T2.NHCAED
    AND T1.NHAGTY = T2.NHAGTY
    AND T1.NHCANO > T2.NHCANO 

    WHERE (
        T1.NHEADT BETWEEN {bolw} AND {eolw} 
        OR T1.NHMODT BETWEEN {bolw} AND {eolw} 
    )
    AND T1.NHCAED >= {today}
    AND T2.NHCAED >= {today}
    AND T1.NHAGTY IN (*TYPES*)
''')

inco_overlaps = customer_incentives_overlaps.replace("*TYPES*", "'INCO'")

admin_overlaps = customer_incentives_overlaps.replace("*TYPES*", "'ASR1','ASR2','ASR3','ASR4'")

drop_overlaps = customer_incentives_overlaps.replace("*TYPES*", "'DPI1','DPI2','DPI3','DPI4','DPI5','DPI6','DPA1','DPA2','DPA3','DPA4','DRUP','EDCP'")
  
volume_overlaps = customer_incentives_overlaps.replace("*TYPES*", "'BDS1','BDS2','BDS3','BDS4','BDV1','BDV2','BDV3','BDV4','BDV5','BDV6','BDV7','BDV8','VPR1','VPR2','VPR3','VPR4','VPR5','VPR6','VPR7','VPR8'")

licg_overlaps = customer_incentives_overlaps.replace("*TYPES*", "'LICG'")

charge_overlaps = customer_incentives_overlaps.replace("*TYPES*", "'UPCH','LASU'")
    
expiring_deals = (f'''
    SELECT
    TRIM(NHARCO) AS SITE, 
    '*MARKET*' AS MARKET,
    ACCOUNT_TYPE,
    NHCANO AS CA_NO,
    TRIM(NHCADC) AS CA_DESCRIPTION,
    NHAGTY AS AGMT_TYPE,
    NHORIG AS ORIGINATOR,
    NHAAPF AS ADJ_AP_FLAG,
    NHACBF AS ADJ_COMM_BASE_FLAG,
    NHPFDB AS PERF_AGMT_DROP_SZ_BASIS_CODE,
    NHAPTY AS APP_TYPE,
    NHCASD AS CA_START,
    NHCAED AS CA_END,
    NHLAWD AS LAST_AWARD_DATE,
    NHNAWD AS NEXT_AWARD_DATE,
    NHAPPI AS APPROVAL_ID,
    NHAPPS AS APPROVAL_STATUS,
    NHAPDT AS APPROVAL_DATE,
    NHEADT AS CREATE_DATE,
    NHEATM AS CREATE_TIME,
    NHEAID AS CREATE_ID,
    NHMODT AS MOD_DATE,
    NHMOTM AS MOD_TIME,
    NHMOID AS MOD_ID

    FROM SCDBFP10.PMPVNHPF

    LEFT JOIN (
        SELECT NHCANO AS CA, MAX(JOACCP) AS ACCOUNT_TYPE
        FROM SCDBFP10.PMPVNHPF

        LEFT JOIN SCDBFP10.PMPZQYPF
        ON NHCANO = QYCANO

        LEFT JOIN SCDBFP10.USCBJOPF
        ON QYCUNO = JOCUNO

        WHERE JOACCP <> ''

        GROUP BY NHCANO
    )
    ON NHCANO = CA

    WHERE (
        NHPPAF = 'PF'
        OR NHAGTY IN ('LICG','UPCH')
    )
    AND NHAGRN = 0
    AND NHCAED BETWEEN {bom} AND {eom}
''')

prompt_overlaps = ''

edfs_overlaps = ''

############################################################################################
# Foodbuy Overlapping Agreements
############################################################################################

foodbuy_overlap_header_sus = f"""
    SELECT
    'VA',
    CAST(FBUY_VA AS VARCHAR(11)) AS FOODBUY_AGREEMENT,
    TRIM(FOODBUY.M7VAGD) AS FBUY_DESCRIPTION,
    LEFT(RIGHT(FOODBUY.M7VASD,4),2) || '/' || RIGHT(FOODBUY.M7VASD,2) ||'/' || LEFT(FOODBUY.M7VASD,4) AS FBUY_START,
    LEFT(RIGHT(FOODBUY.M7VAED,4),2) || '/' || RIGHT(FOODBUY.M7VAED,2) ||'/' || LEFT(FOODBUY.M7VAED,4) AS FBUY_END,
    CAST(DIRECT_VA AS VARCHAR(11)) AS DIRECT_AGREEMENT,
    TRIM(DIRECT.M7VAGD) AS DIRECT_DESCRIPTION,
    LEFT(RIGHT(DIRECT.M7VASD,4),2) || '/' || RIGHT(DIRECT.M7VASD,2) ||'/' || LEFT(DIRECT.M7VASD,4) AS DIRECT_START,
    LEFT(RIGHT(DIRECT.M7VAED,4),2) || '/' || RIGHT(DIRECT.M7VAED,2) ||'/' || LEFT(DIRECT.M7VAED,4) AS DIRECT_END,
    CASE
        WHEN FOODBUY_OVERRIDE.NKPANO IS NOT NULL THEN 'FOODBUY'
        WHEN DIRECT_OVERRIDE.NKPANO IS NOT NULL THEN 'DIRECT'
        WHEN FOODBUY_CA.NHAGTP = 'D' OR DIRECT_CA.NHAGTP = 'D' THEN 'BOTH'
        WHEN FOODBUY.M7APDT > DIRECT.M7APDT THEN 'FOODBUY (NOT SET)'
        ELSE 'DIRECT (NOT SET)'
    END AS APPLIED_PRICING,
    '{timestamp}' AS TIMESTAMP

    FROM (

        SELECT DISTINCT
        FOODBUY.LOCAL_VA AS FBUY_VA,
        DIRECT.LOCAL_VA AS DIRECT_VA

        FROM (

            SELECT
            HEADER.VA AS LOCAL_VA,
            ITEM.SUPC

            FROM (
                SELECT DISTINCT
                M7VAGN AS VA

                FROM SCDBFP10.PMVHM7PF

                WHERE M7AGRN = 999999999
                AND M7VAED >= {today}
            ) AS HEADER

            INNER JOIN (
                SELECT
                QBVAGN AS LOCAL_VA,
                QBITEM AS SUPC

                FROM SCDBFP10.PMPZQBPF

                WHERE QBEFED >= {today}
            ) AS ITEM
            ON HEADER.VA = ITEM.LOCAL_VA
        ) AS FOODBUY

        INNER JOIN (

            SELECT
            HEADER.VA AS LOCAL_VA,
            ITEM.SUPC

            FROM (
                SELECT DISTINCT
                M7VAGN AS VA

                FROM SCDBFP10.PMVHM7PF

                WHERE M7AGRN <> 999999999
                AND M7VAED >= {today}
            ) AS HEADER

            INNER JOIN (
                SELECT
                QBVAGN AS LOCAL_VA,
                QBITEM AS SUPC

                FROM SCDBFP10.PMPZQBPF

                WHERE QBEFED >= {today}
            ) AS ITEM
            ON HEADER.VA = ITEM.LOCAL_VA
        ) AS DIRECT
        ON FOODBUY.SUPC = DIRECT.SUPC

        INNER JOIN (

            SELECT DISTINCT
            FOODBUY.LOCAL_VA AS FOODBUY_VA,
            DIRECT.LOCAL_VA AS DIRECT_VA

            FROM (

                SELECT
                HEADER.VA AS LOCAL_VA,
                CUSTOMER.SHIP_TO

                FROM (
                    SELECT DISTINCT
                    M7VAGN AS VA

                    FROM SCDBFP10.PMVHM7PF

                    WHERE M7AGRN = 999999999
                    AND M7VAED >= {today}
                ) AS HEADER

                INNER JOIN (
                    SELECT
                    QWVAGN AS LOCAL_VA,
                    QWCUNO AS SHIP_TO

                    FROM SCDBFP10.PMPZQWPF

                    WHERE QWEFED >= {today}
                ) AS CUSTOMER
                ON HEADER.VA = CUSTOMER.LOCAL_VA

            ) AS FOODBUY

            INNER JOIN (

                SELECT
                HEADER.VA AS LOCAL_VA,
                CUSTOMER.SHIP_TO

                FROM (
                    SELECT DISTINCT
                    M7VAGN AS VA

                    FROM SCDBFP10.PMVHM7PF

                    WHERE M7AGRN <> 999999999
                    AND M7VAED >= {today}
                ) AS HEADER

                INNER JOIN (
                    SELECT
                    QWVAGN AS LOCAL_VA,
                    QWCUNO AS SHIP_TO

                    FROM SCDBFP10.PMPZQWPF

                    WHERE QWEFED >= {today}
                ) AS CUSTOMER
                ON HEADER.VA = CUSTOMER.LOCAL_VA
            ) AS DIRECT
            ON FOODBUY.SHIP_TO = DIRECT.SHIP_TO
        ) AS CUSTOMER_OVERLAP
        ON FOODBUY.LOCAL_VA = CUSTOMER_OVERLAP.FOODBUY_VA
        AND DIRECT.LOCAL_VA = CUSTOMER_OVERLAP.DIRECT_VA
    )

    LEFT JOIN SCDBFP10.PMVHM7PF AS FOODBUY
    ON FBUY_VA = FOODBUY.M7VAGN

    LEFT JOIN SCDBFP10.PMVHM7PF AS DIRECT
    ON DIRECT_VA = DIRECT.M7VAGN

    LEFT JOIN SCDBFP10.PMPYNKPF AS FOODBUY_OVERRIDE
    ON FOODBUY.M7VAGN = FOODBUY_OVERRIDE.NKPANO
    AND DIRECT.M7VAGN = FOODBUY_OVERRIDE.NKCOAN
    AND FOODBUY_OVERRIDE.NKVCAF = 'V'

    LEFT JOIN SCDBFP10.PMPYNKPF AS DIRECT_OVERRIDE
    ON DIRECT.M7VAGN = DIRECT_OVERRIDE.NKPANO
    AND FOODBUY.M7VAGN = DIRECT_OVERRIDE.NKCOAN
    AND DIRECT_OVERRIDE.NKVCAF = 'V'

    LEFT JOIN SCDBFP10.PMPVNHPF AS FOODBUY_CA
    ON FOODBUY.M7ACAN = FOODBUY_CA.NHCANO

    LEFT JOIN SCDBFP10.PMPVNHPF AS DIRECT_CA
    ON DIRECT.M7ACAN = DIRECT_CA.NHCANO

    WHERE DIRECT.M7VASD <= FOODBUY.M7VAED
    AND DIRECT.M7VAED >= FOODBUY.M7VASD
    AND DIRECT.M7VAGD NOT LIKE '%REPORTING FEE%'
    AND DIRECT.M7VAGD NOT LIKE '%NATIONAL PRICING%'
    AND DIRECT.M7VAGD NOT LIKE '%BLANKET%'

    ORDER BY
    FBUY_VA,
    DIRECT_VA

    LIMIT 1000
"""

def foodbuy_overlap_item_sus(foodbuy_agreements, direct_agreements):
    return f"""
        SELECT
        'VA',
        CAST(FOODBUY_HEADER.M7VAGN AS VARCHAR(11)),
        TRIM(FOODBUY_HEADER.M7VAGD) AS FBUY_DESCRIPTION,
        LEFT(RIGHT(FOODBUY_HEADER.M7VASD,4),2) || '/' || RIGHT(FOODBUY_HEADER.M7VASD,2) ||'/' || LEFT(FOODBUY_HEADER.M7VASD,4) AS FBUY_START,
        LEFT(RIGHT(FOODBUY_HEADER.M7VAED,4),2) || '/' || RIGHT(FOODBUY_HEADER.M7VAED,2) ||'/' || LEFT(FOODBUY_HEADER.M7VAED,4) AS FBUY_END,
        CAST(DIRECT_HEADER.M7VAGN AS VARCHAR(11)),
        TRIM(DIRECT_HEADER.M7VAGD) AS DIRECT_DESCRIPTION,
        LEFT(RIGHT(DIRECT_HEADER.M7VASD,4),2) || '/' || RIGHT(DIRECT_HEADER.M7VASD,2) ||'/' || LEFT(DIRECT_HEADER.M7VASD,4) AS DIRECT_START,
        LEFT(RIGHT(DIRECT_HEADER.M7VAED,4),2) || '/' || RIGHT(DIRECT_HEADER.M7VAED,2) ||'/' || LEFT(DIRECT_HEADER.M7VAED,4) AS DIRECT_END,
        TRIM(FOODBUY_ITEM.SUPC) AS SUPC,
        TRIM(JFITDS) AS ITEM_DESCRIPTION,
        '{timestamp}' AS TIMESTAMP

        FROM (
            SELECT DISTINCT
            QBVAGN AS VA, 
            QBITEM AS SUPC, 
            QBEFSD AS EFF_DT,
            QBEFED AS END_DT

            FROM SCDBFP10.PMPZQBPF

            WHERE QBVAGN IN ({foodbuy_agreements})
        ) AS FOODBUY_ITEM

        INNER JOIN (
            SELECT DISTINCT
            QBVAGN AS VA, 
            QBITEM AS SUPC, 
            QBEFSD AS EFF_DT,
            QBEFED AS END_DT

            FROM SCDBFP10.PMPZQBPF

            WHERE QBVAGN IN ({direct_agreements})
        ) AS DIRECT_ITEM
        ON FOODBUY_ITEM.SUPC = DIRECT_ITEM.SUPC
        AND FOODBUY_ITEM.EFF_DT <= DIRECT_ITEM.END_DT
        AND FOODBUY_ITEM.END_DT >= DIRECT_ITEM.EFF_DT

        LEFT JOIN SCDBFP10.PMVHM7PF AS FOODBUY_HEADER
        ON FOODBUY_ITEM.VA = FOODBUY_HEADER.M7VAGN

        LEFT JOIN SCDBFP10.PMVHM7PF AS DIRECT_HEADER
        ON DIRECT_ITEM.VA = DIRECT_HEADER.M7VAGN

        LEFT JOIN SCDBFP10.USIAJFPF
        ON FOODBUY_ITEM.SUPC = JFITEM

        WHERE DIRECT_HEADER.M7VAGD NOT LIKE '%REPORTING FEE%'
        AND DIRECT_HEADER.M7VAGD NOT LIKE '%NATIONAL PRICING%'
        AND DIRECT_HEADER.M7VAGD NOT LIKE '%BLANKET%'

        ORDER BY
        FOODBUY_HEADER.M7VAGN,
        DIRECT_HEADER.M7VAGN,
        FOODBUY_ITEM.SUPC
    """


def foodbuy_overlap_customer_sus (foodbuy_agreements, direct_agreements):
    return f"""
        SELECT 
        TRIM(FOODBUY_HEADER.M7ARCO) AS SITE,
        TRIM(LEFT(REFDAT, LOCATE('YN', REFDAT)-1)) AS SITE_NAME,
        'VA',
        CAST(FOODBUY_CUSTOMER.VA AS VARCHAR(11)),
        TRIM(FOODBUY_HEADER.M7VAGD) AS FBUY_DESCRIPTION,
        LEFT(RIGHT(FOODBUY_HEADER.M7VASD,4),2) || '/' || RIGHT(FOODBUY_HEADER.M7VASD,2) ||'/' || LEFT(FOODBUY_HEADER.M7VASD,4) AS FBUY_START,
        LEFT(RIGHT(FOODBUY_HEADER.M7VAED,4),2) || '/' || RIGHT(FOODBUY_HEADER.M7VAED,2) ||'/' || LEFT(FOODBUY_HEADER.M7VAED,4) AS FBUY_END,
        CAST(DIRECT_CUSTOMER.VA AS VARCHAR(11)),
        TRIM(DIRECT_HEADER.M7VAGD) AS DIRECT_DESCRIPTION,
        LEFT(RIGHT(DIRECT_HEADER.M7VASD,4),2) || '/' || RIGHT(DIRECT_HEADER.M7VASD,2) ||'/' || LEFT(DIRECT_HEADER.M7VASD,4) AS DIRECT_START,
        LEFT(RIGHT(DIRECT_HEADER.M7VAED,4),2) || '/' || RIGHT(DIRECT_HEADER.M7VAED,2) ||'/' || LEFT(DIRECT_HEADER.M7VAED,4) AS DIRECT_END,
        TRIM(DIRECT_CUSTOMER.CUSTOMER) AS DCN,
        REPLACE(TRIM(CUNAME),'''','') AS CUSTOMER_NAME,
        '{timestamp}' AS TIMESTAMP

        FROM (
            SELECT DISTINCT
            QWVAGN AS VA, 
            QWCUNO AS CUSTOMER, 
            QWEFSD AS EFF_DT,
            QWEFED AS END_DT

            FROM SCDBFP10.PMPZQWPF

            WHERE QWVAGN IN ({foodbuy_agreements})
        ) AS FOODBUY_CUSTOMER

        INNER JOIN (
            SELECT DISTINCT
            QWVAGN AS VA, 
            QWCUNO AS CUSTOMER, 
            QWEFSD AS EFF_DT,
            QWEFED AS END_DT

            FROM SCDBFP10.PMPZQWPF

            WHERE QWVAGN IN ({direct_agreements})
        ) AS DIRECT_CUSTOMER
        ON FOODBUY_CUSTOMER.CUSTOMER = DIRECT_CUSTOMER.CUSTOMER
        AND FOODBUY_CUSTOMER.EFF_DT <= DIRECT_CUSTOMER.END_DT
        AND FOODBUY_CUSTOMER.END_DT >= DIRECT_CUSTOMER.EFF_DT

        LEFT JOIN SCDBFP10.PMVHM7PF AS FOODBUY_HEADER
        ON FOODBUY_CUSTOMER.VA = FOODBUY_HEADER.M7VAGN

        LEFT JOIN SCDBFP10.PMVHM7PF AS DIRECT_HEADER
        ON DIRECT_CUSTOMER.VA = DIRECT_HEADER.M7VAGN

        LEFT JOIN ARDBFA.ARPCU
        ON DIRECT_CUSTOMER.CUSTOMER = CUCUNO

        LEFT JOIN SCDBFP10.REFERP
        ON FOODBUY_HEADER.M7ARCO = REFKEY
        AND REFCAT = 'DM '

        WHERE DIRECT_HEADER.M7VAGD NOT LIKE '%REPORTING FEE%'
        AND DIRECT_HEADER.M7VAGD NOT LIKE '%NATIONAL PRICING%'
        AND DIRECT_HEADER.M7VAGD NOT LIKE '%BLANKET%'

        ORDER BY
        FOODBUY_CUSTOMER.VA,
        DIRECT_CUSTOMER.VA,
        DIRECT_CUSTOMER.CUSTOMER
    """

foodbuy_overlap_header_server = F"""
    SELECT DISTINCT
    OVERLAP_TYPE AS [TYPE],
    '' AS [TERM SET CODE], 
    '' AS [TERM SET NAME],
    FOODBUY_AGREEMENT AS [FBUY AGMT#],
    FOODBUY_DESCRIPTION AS [FBUY AGMT DESCRIPTION],
    FORMAT(FOODBUY_START, 'MM/dd/yyyy') AS [FBUY START], 
    FORMAT(FOODBUY_END, 'MM/dd/yyyy') AS [FBUY END],
    DIRECT_AGREEMENT AS [DIRECT AGMT#],
    DIRECT_DESCRIPTION AS [DIRECT AGMT DESCRIPTION],
    FORMAT(DIRECT_START, 'MM/dd/yyyy') AS [DIRECT START], 
    FORMAT(DIRECT_END, 'MM/dd/yyyy') AS [DIRECT END],
    APPLIED_PRICING AS [APPLIED PRICING]

    FROM Foodbuy_Overlap_Header

    WHERE TIMESTAMP = '{timestamp}'
"""

foodbuy_overlap_item_server = f"""
    SELECT DISTINCT
    OVERLAP_TYPE AS [TYPE],
    '' AS [TERM SET CODE], 
    '' AS [TERM SET NAME],
    FOODBUY_AGREEMENT AS [FBUY AGMT#],
    FOODBUY_DESCRIPTION AS [FBUY AGMT DESCRIPTION],
    FORMAT(FOODBUY_START, 'MM/dd/yyyy') AS [FBUY START], 
    FORMAT(FOODBUY_END, 'MM/dd/yyyy') AS [FBUY END],
    DIRECT_AGREEMENT AS [DIRECT AGMT#],
    DIRECT_DESCRIPTION AS [DIRECT AGMT DESCRIPTION],
    FORMAT(DIRECT_START, 'MM/dd/yyyy') AS [DIRECT START], 
    FORMAT(DIRECT_END, 'MM/dd/yyyy') AS [DIRECT END],
    ITEM AS [SUPC], 
    ITEM_DESCRIPTION AS [ITEM DESCRIPTION]

    FROM Foodbuy_Overlap_Item

    WHERE TIMESTAMP = '{timestamp}'
"""

foodbuy_overlap_customer_server = f"""
    SELECT 
    SITE_NBR AS [SITE],
    SITE_NAME AS [SITE NAME],
    OVERLAP_TYPE AS [TYPE],
    '' AS [TERM SET CODE], 
    '' AS [TERM SET NAME],
    FOODBUY_AGREEMENT AS [FBUY AGMT#],
    FOODBUY_DESCRIPTION AS [FBUY AGMT DESCRIPTION],
    FORMAT(FOODBUY_START, 'MM/dd/yyyy') AS [FBUY START], 
    FORMAT(FOODBUY_END, 'MM/dd/yyyy') AS [FBUY END],
    DIRECT_AGREEMENT AS [DIRECT AGMT#],
    DIRECT_DESCRIPTION AS [DIRECT AGMT DESCRIPTION],
    FORMAT(DIRECT_START, 'MM/dd/yyyy') AS [DIRECT START], 
    FORMAT(DIRECT_END, 'MM/dd/yyyy') AS [DIRECT END],
    DCN, 
    CUSTOMER_NAME AS [CUSTOMER NAME]

    FROM Foodbuy_Overlap_Customer

    WHERE TIMESTAMP = '{timestamp}'
"""

foodbuy_server_cleanup = """
    BEGIN TRANSACTION 

    DELETE 

    FROM FOODBUY_OVERLAP_HEADER

    WHERE PRIMARY_KEY NOT IN (

        SELECT MAX(PRIMARY_KEY)

        FROM FOODBUY_OVERLAP_HEADER

        GROUP BY 
        FOODBUY_AGREEMENT, 
        DIRECT_AGREEMENT
    )

    DELETE 

    FROM Foodbuy_Overlap_Item

    WHERE PRIMARY_KEY NOT IN (

        SELECT MAX(PRIMARY_KEY)

        FROM Foodbuy_Overlap_Item

        GROUP BY 
        FOODBUY_AGREEMENT, 
        DIRECT_AGREEMENT, 
        ITEM
    )

    COMMIT
"""

############################################################################################
# Daily rebate basis validation
############################################################################################

rebate_basis_validation = (f"""
    SELECT * FROM (
        SELECT
        NHCVAN AS VA, 
        NHCANO AS CA, 
        TRIM(NHCADC) AS DESCRIPTION, 
        NHAGTY AS TYPE, 
        NHCASD AS EFFECTIVE_DT, 
        NHCAED AS END_DT, 
        TRIM(QXITEM) AS ITEM, 
        JFLCCT AS CATEGORY, 
        TRIM(JFITDS) AS ITEM_DESCRIPTION,
        QXACBS AS REBATE_BASIS,
        QXXAMT AS ALLOWANCE_AMT,
        QXCBAJ AS COMM_BASE,
        QXAPAJ AS AP_ADJ,
        TRIM(NHEAID) AS CREATE_ID,
        CASE
            WHEN QXACBS IN ('CC', 'LC') AND QXAPAJ < 10 AND JFLCCT <> 11 AND JFITDS NOT LIKE '%DISPENSER%' AND JFITDS NOT LIKE '%LABEL%' THEN 'PRICE/CS < $10'
            WHEN QXACBS = 'GC' AND QXXAMT < 10 AND JFLCCT <> 11 AND JFITDS NOT LIKE '%DISPENSER%' AND JFITDS NOT LIKE '%LABEL%' THEN 'PRICE/CS < $10'
            WHEN QXACBS IN ('CP','LP') AND QXAPAJ > 15 AND JFLCCT <> 3 THEN 'PRICE/LB > $15'
            WHEN QXACBS = 'GP' AND QXXAMT > 15 AND JFLCCT <> 3 THEN 'PRICE/LB > $15'       
            WHEN QXACBS IN ('CP','LP') AND QXAPAJ > 20 AND JFLCCT = 3 THEN 'PRICE/LB > $20 (CAT03)'
            WHEN QXACBS = 'GP' AND QXXAMT > 20 AND JFLCCT = 3 THEN 'PRICE/LB > $20 (CAT03)'
            WHEN QXACBS = 'DC' AND QXXAMT > 10 AND NHAGTY NOT IN ('SFCA', 'BASE') THEN 'OFF/CS > $10'
            WHEN QXACBS = 'DP' AND QXXAMT > 5 AND NHAGTY NOT IN ('SFCA','BASE') THEN 'OFF/LB > $5'
            WHEN QXACBS IN ('DC', 'DP') AND (QXAPAJ = 0 OR QXCBAJ = 0 OR QXAPAJ = 0) THEN 'NO ALLOWANCE TO CUSTOMER'
        END AS ERROR

        FROM SCDBFP10.PMPVNHPF

        LEFT JOIN SCDBFP10.PMPZQXPF
        ON NHCANO = QXCANO

        INNER JOIN SCDBFP10.USIAJFPF
        ON QXITEM = JFITEM

        WHERE NHEADT = {today}
        AND NHPPAF = 'PD'
        AND NOT NHAGTY IN ('LICG', 'UPCH')
        AND NOT (NHAPNM LIKE '%DPMEI%' AND NHAGTY = 'SFVA')
    )
    WHERE ERROR IS NOT NULL
""")

############################################################################################
# Server jobs
############################################################################################

cal_backup = (f"""
    BEGIN TRANSACTION 

    DELETE FROM CAL_Account_Assignments_BACKUP WHERE TIMESTAMP < '{last_month}'
    DELETE FROM CAL_Customer_Profile_BACKUP WHERE TIMESTAMP < '{last_month}'
    DELETE FROM CAL_Programs_BACKUP WHERE TIMESTAMP < '{last_month}'

    INSERT INTO CAL_Programs_BACKUP 

    SELECT 
    DAB,
    CUSTOMER,
    PROGRAM_DESCRIPTION,
    START_DATE,
    END_DATE,
    LEAD_VA,
    LEAD_CA,
    VEND_AGMT_TYPE,
    VENDOR_NUM,
    COST_BASIS,
    CUST_AGMT_TYPE,
    REBATE_BASIS,
    PRE_APPROVAL,
    APPROP_NAME,
    PRN_GRP,
    PACKET,
    PACKET_DL,
    COMMENTS,
    EXTENDED_COMMENTS,
    '{timestamp}'

    FROM CAL_Programs

    INSERT INTO CAL_Customer_Profile_BACKUP

    SELECT 
    CUSTOMER,
    ALT_NAME,
    PACKET,
    PRICE_RULE,
    NID,
    MASTER_PRN,
    PRICING_PRN,
    GROUP_NAME,
    VPNA,
    NAM,
    CUST_CONTACT,
    OT_URL,
    NOTES,
    '{timestamp}'

    FROM CAL_Customer_Profile

    INSERT INTO CAL_Account_Assignments_BACKUP

    SELECT 
    CUSTOMER_NAME,
    ALT_NAME,
    ASS_NOTES,
    TEAM_LEAD,
    TIER_1,
    TIER_2,
    TIER_3,
    GPO,
    PACKET,
    PROGRAM_COUNT,
    NID,
    GPO_TIE,
    CUST_TYPE,
    WEEKLY,
    WEEKLY_COUNT,
    NOTES,
    LEAD_HOUSE,
    LEAD_ID,
    T1_ID,
    T2_ID,
    T3_ID,
    '{timestamp}'

    FROM CAL_Account_Assignments

    COMMIT
""")