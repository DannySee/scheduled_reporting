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

updl_violation = (f'''
    SELECT
    TRIM(NHARCO) AS SITE,
    NHCANO AS CA,
    TRIM(NHCADC) AS DESCRIPTION,
    NHCASD AS START_DT,
    NHCAED AS END_DT,
    NHPFRB AS REBATE_BASIS

    FROM SCDBFP10.PMPVNHPF

    INNER JOIN SCDBFP10.PMPZO5L0 AS T2
    ON NHCANO = O5CANO

    WHERE NHEADT = {yesterday}
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
    NHARCO AS SITE, 
    ACCOUNT_TYPE,
    NHCANO AS CA_NO,
    NHCADC AS CA_DESCRIPTION,
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

    WHERE (NHPPAF IN ('PF')
    OR NHAGTY IN ('LICG','UPCH'))
    AND NHAGRN = 0
    AND NHCAED BETWEEN {bom} AND {eom}
''')

prompt_overlaps = ''

edfs_overlaps = ''

############################################################################################
# Foodbuy Overlapping Agreements
############################################################################################

overlap_header_sus = (f"""
SELECT
'VA',
CAST(FBUY_VA AS VARCHAR(11)),
TRIM(FOODBUY.M7VAGD) AS FBUY_DESCRIPTION,
LEFT(RIGHT(FOODBUY.M7VASD,4),2) || '/' || RIGHT(FOODBUY.M7VASD,2) ||'/' || LEFT(FOODBUY.M7VASD,4) AS FBUY_START,
LEFT(RIGHT(FOODBUY.M7VAED,4),2) || '/' || RIGHT(FOODBUY.M7VAED,2) ||'/' || LEFT(FOODBUY.M7VAED,4) AS FBUY_END,
CAST(DIRECT_VA AS VARCHAR(11)),
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
    FOODBUY.LEAD_VA AS FBUY_VA,
    DIRECT.LEAD_VA AS DIRECT_VA

    FROM (

        SELECT
        M7AGRN AS LEAD_VA,
        M7VAGN AS LOCAL_VA,
        ITEM.SUPC

        FROM (
            SELECT DISTINCT
            CAST(TRIM(BJELEN) AS INT) AS VA

            FROM SCDBFP10.PMFDBJV1

            WHERE BJDPNM LIKE '%FOODBUY%'
            AND LEFT(BJBIE1,2) = 'VA'
            AND UPPER(BJELEN) = LOWER(BJELEN)
            AND BJELEN IS NOT NULL
            AND TRIM(BJELEN) <> ''
        ) AS HEADER

        INNER JOIN SCDBFP10.PMVHM7PF
        ON HEADER.VA = M7AGRN
        AND M7EADT >= {bolw}

        INNER JOIN (
            SELECT
            QBVAGN AS LOCAL_VA,
            QBITEM AS SUPC

            FROM SCDBFP10.PMPZQBPF

            WHERE QBEFED >= {today}
        ) AS ITEM
        ON M7VAGN = ITEM.LOCAL_VA
    ) AS FOODBUY

    INNER JOIN (

        SELECT
        M7AGRN AS LEAD_VA,
        M7VAGN LOCAL_VA,
        ITEM.SUPC

        FROM (
            SELECT DISTINCT
            CAST(TRIM(BJELEN) AS INT) AS VA

            FROM SCDBFP10.PMFDBJV1

            WHERE BJDPNM NOT LIKE '%FOODBUY%'
            AND LEFT(BJBIE1,2) = 'VA'
            AND UPPER(BJELEN) = LOWER(BJELEN)
            AND BJELEN IS NOT NULL
            AND TRIM(BJELEN) <> ''
        ) AS HEADER

        INNER JOIN SCDBFP10.PMVHM7PF
        ON HEADER.VA = M7AGRN
        AND M7EADT >= {bolw}

        INNER JOIN (
            SELECT
            QBVAGN AS LOCAL_VA,
            QBITEM AS SUPC

            FROM SCDBFP10.PMPZQBPF

            WHERE QBEFED >= {today}
        ) AS ITEM
        ON M7VAGN = ITEM.LOCAL_VA
    ) AS DIRECT
    ON FOODBUY.SUPC = DIRECT.SUPC

    INNER JOIN (

        SELECT DISTINCT
        FOODBUY.LEAD_VA AS FOODBUY_VA,
        DIRECT.LEAD_VA AS DIRECT_VA

        FROM (

            SELECT
            M7AGRN AS LEAD_VA,
            M7VAGN AS LOCAL_VA,
            CUSTOMER.SHIP_TO

            FROM (
                SELECT DISTINCT
                CAST(TRIM(BJELEN) AS INT) AS VA

                FROM SCDBFP10.PMFDBJV1

                WHERE BJDPNM LIKE '%FOODBUY%'
                AND LEFT(BJBIE1,2) = 'VA'
                AND UPPER(BJELEN) = LOWER(BJELEN)
                AND BJELEN IS NOT NULL
                AND TRIM(BJELEN) <> ''
            ) AS HEADER

            INNER JOIN SCDBFP10.PMVHM7PF
            ON HEADER.VA = M7AGRN
            AND M7EADT >= {bolw}

            INNER JOIN (
                SELECT
                QWVAGN AS LOCAL_VA,
                QWCUNO AS SHIP_TO

                FROM SCDBFP10.PMPZQWPF

                WHERE QWEFED >= {today}
            ) AS CUSTOMER
            ON M7VAGN = CUSTOMER.LOCAL_VA

        ) AS FOODBUY

        INNER JOIN (

            SELECT
            M7AGRN AS LEAD_VA,
            M7VAGN AS LOCAL_VA,
            CUSTOMER.SHIP_TO

            FROM (
                SELECT DISTINCT
                CAST(TRIM(BJELEN) AS INT) AS VA

                FROM SCDBFP10.PMFDBJV1

                WHERE BJDPNM NOT LIKE '%FOODBUY%'
                AND LEFT(BJBIE1,2) = 'VA'
                AND UPPER(BJELEN) = LOWER(BJELEN)
                AND BJELEN IS NOT NULL
                AND TRIM(BJELEN) <> ''
            ) AS HEADER

            INNER JOIN SCDBFP10.PMVHM7PF
            ON HEADER.VA = M7AGRN
            AND M7EADT >={bolw}

            INNER JOIN (
                SELECT
                QWVAGN AS LOCAL_VA,
                QWCUNO AS SHIP_TO

                FROM SCDBFP10.PMPZQWPF

                WHERE QWEFED >= {today}
            ) AS CUSTOMER
            ON M7VAGN = CUSTOMER.LOCAL_VA
        ) AS DIRECT
        ON FOODBUY.SHIP_TO = DIRECT.SHIP_TO
    ) AS CUSTOMER_OVERLAP
    ON FOODBUY.LEAD_VA = CUSTOMER_OVERLAP.FOODBUY_VA
    AND DIRECT.LEAD_VA = CUSTOMER_OVERLAP.DIRECT_VA
)

LEFT JOIN SCDBFP10.PMVHM7PF AS FOODBUY
ON FBUY_VA = FOODBUY.M7AGRN

LEFT JOIN SCDBFP10.PMVHM7PF AS DIRECT
ON DIRECT_VA = DIRECT.M7AGRN

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
AND FOODBUY.M7AGRN <> 749911
AND DIRECT.M7VAGD NOT LIKE '%REPORTING FEE%'
AND DIRECT.M7VAGD NOT LIKE '%NATIONAL PRICING%'
AND DIRECT.M7VAGD NOT LIKE '%BLANKET%'

ORDER BY
FBUY_VA,
DIRECT_VA

LIMIT 1000
""")

overlap_item_sus = (f"""
SELECT
'VA',
CAST(FBUY_VA AS VARCHAR(11)),
TRIM(FOODBUY.M7VAGD) AS FBUY_DESCRIPTION,
LEFT(RIGHT(FOODBUY.M7VASD,4),2) || '/' || RIGHT(FOODBUY.M7VASD,2) ||'/' || LEFT(FOODBUY.M7VASD,4) AS FBUY_START,
LEFT(RIGHT(FOODBUY.M7VAED,4),2) || '/' || RIGHT(FOODBUY.M7VAED,2) ||'/' || LEFT(FOODBUY.M7VAED,4) AS FBUY_END,
CAST(DIRECT_VA AS VARCHAR(11)),
TRIM(DIRECT.M7VAGD) AS DIRECT_DESCRIPTION,
LEFT(RIGHT(DIRECT.M7VASD,4),2) || '/' || RIGHT(DIRECT.M7VASD,2) ||'/' || LEFT(DIRECT.M7VASD,4) AS DIRECT_START,
LEFT(RIGHT(DIRECT.M7VAED,4),2) || '/' || RIGHT(DIRECT.M7VAED,2) ||'/' || LEFT(DIRECT.M7VAED,4) AS DIRECT_END,
TRIM(SUPC) AS SUPC,
TRIM(JFITDS) AS ITEM_DESCRIPTION,
'{timestamp}' AS TIMESTAMP

FROM (

    SELECT DISTINCT
    FOODBUY.LEAD_VA AS FBUY_VA,
    DIRECT.LEAD_VA AS DIRECT_VA,
    FOODBUY.SUPC

    FROM (

        SELECT
        M7AGRN AS LEAD_VA,
        M7VAGN AS LOCAL_VA,
        ITEM.SUPC

        FROM (
            SELECT DISTINCT
            CAST(TRIM(BJELEN) AS INT) AS VA

            FROM SCDBFP10.PMFDBJV1

            WHERE BJDPNM LIKE '%FOODBUY%'
            AND LEFT(BJBIE1,2) = 'VA'
            AND UPPER(BJELEN) = LOWER(BJELEN)
            AND BJELEN IS NOT NULL
            AND TRIM(BJELEN) <> ''
        ) AS HEADER

        INNER JOIN SCDBFP10.PMVHM7PF
        ON HEADER.VA = M7AGRN
        AND M7EADT >= {bolw}

        INNER JOIN (
            SELECT
            QBVAGN AS LOCAL_VA,
            QBITEM AS SUPC

            FROM SCDBFP10.PMPZQBPF

            WHERE QBEFED >= {today}
        ) AS ITEM
        ON M7VAGN = ITEM.LOCAL_VA
    ) AS FOODBUY

    INNER JOIN (

        SELECT
        M7AGRN AS LEAD_VA,
        M7VAGN LOCAL_VA,
        ITEM.SUPC

        FROM (
            SELECT DISTINCT
            CAST(TRIM(BJELEN) AS INT) AS VA

            FROM SCDBFP10.PMFDBJV1

            WHERE BJDPNM NOT LIKE '%FOODBUY%'
            AND LEFT(BJBIE1,2) = 'VA'
            AND UPPER(BJELEN) = LOWER(BJELEN)
            AND BJELEN IS NOT NULL
            AND TRIM(BJELEN) <> ''
        ) AS HEADER

        INNER JOIN SCDBFP10.PMVHM7PF
        ON HEADER.VA = M7AGRN
        AND M7EADT >= {bolw}

        INNER JOIN (
            SELECT
            QBVAGN AS LOCAL_VA,
            QBITEM AS SUPC

            FROM SCDBFP10.PMPZQBPF

            WHERE QBEFED >= {today}
        ) AS ITEM
        ON M7VAGN = ITEM.LOCAL_VA
    ) AS DIRECT
    ON FOODBUY.SUPC = DIRECT.SUPC

    INNER JOIN (

        SELECT DISTINCT
        FOODBUY.LEAD_VA AS FOODBUY_VA,
        DIRECT.LEAD_VA AS DIRECT_VA

        FROM (

            SELECT
            M7AGRN AS LEAD_VA,
            M7VAGN AS LOCAL_VA,
            CUSTOMER.SHIP_TO

            FROM (
                SELECT DISTINCT
                CAST(TRIM(BJELEN) AS INT) AS VA

                FROM SCDBFP10.PMFDBJV1

                WHERE BJDPNM LIKE '%FOODBUY%'
                AND LEFT(BJBIE1,2) = 'VA'
                AND UPPER(BJELEN) = LOWER(BJELEN)
                AND BJELEN IS NOT NULL
                AND TRIM(BJELEN) <> ''
            ) AS HEADER

            INNER JOIN SCDBFP10.PMVHM7PF
            ON HEADER.VA = M7AGRN
            AND M7EADT >= {bolw}

            INNER JOIN (
                SELECT
                QWVAGN AS LOCAL_VA,
                QWCUNO AS SHIP_TO

                FROM SCDBFP10.PMPZQWPF

                WHERE QWEFED >= {today}
            ) AS CUSTOMER
            ON M7VAGN = CUSTOMER.LOCAL_VA

        ) AS FOODBUY

        INNER JOIN (

            SELECT
            M7AGRN AS LEAD_VA,
            M7VAGN AS LOCAL_VA,
            CUSTOMER.SHIP_TO

            FROM (
                SELECT DISTINCT
                CAST(TRIM(BJELEN) AS INT) AS VA

                FROM SCDBFP10.PMFDBJV1

                WHERE BJDPNM NOT LIKE '%FOODBUY%'
                AND LEFT(BJBIE1,2) = 'VA'
                AND UPPER(BJELEN) = LOWER(BJELEN)
                AND BJELEN IS NOT NULL
                AND TRIM(BJELEN) <> ''
            ) AS HEADER

            INNER JOIN SCDBFP10.PMVHM7PF
            ON HEADER.VA = M7AGRN
            AND M7EADT >={bolw}

            INNER JOIN (
                SELECT
                QWVAGN AS LOCAL_VA,
                QWCUNO AS SHIP_TO

                FROM SCDBFP10.PMPZQWPF

                WHERE QWEFED >= {today}
            ) AS CUSTOMER
            ON M7VAGN = CUSTOMER.LOCAL_VA
        ) AS DIRECT
        ON FOODBUY.SHIP_TO = DIRECT.SHIP_TO
    ) AS CUSTOMER_OVERLAP
    ON FOODBUY.LEAD_VA = CUSTOMER_OVERLAP.FOODBUY_VA
    AND DIRECT.LEAD_VA = CUSTOMER_OVERLAP.DIRECT_VA
)

LEFT JOIN SCDBFP10.PMVHM7PF AS FOODBUY
ON FBUY_VA = FOODBUY.M7AGRN

LEFT JOIN SCDBFP10.PMVHM7PF AS DIRECT
ON DIRECT_VA = DIRECT.M7AGRN

LEFT JOIN SCDBFP10.USIAJFPF
ON SUPC = JFITEM

WHERE DIRECT.M7VASD <= FOODBUY.M7VAED
AND DIRECT.M7VAED >= FOODBUY.M7VASD
AND FOODBUY.M7AGRN <> 749911
AND DIRECT.M7VAGD NOT LIKE '%REPORTING FEE%'
AND DIRECT.M7VAGD NOT LIKE '%NATIONAL PRICING%'
AND DIRECT.M7VAGD NOT LIKE '%BLANKET%'

ORDER BY
FBUY_VA,
DIRECT_VA,
SUPC

LIMIT 1000
""")

overlap_customer_sus = (f"""
SELECT
TRIM(FOODBUY.M7ARCO) AS SITE,
TRIM(LEFT(REFDAT, LOCATE('YN', REFDAT)-1)) AS SITE_NAME,
'VA',
CAST(FBUY_VA AS VARCHAR(11)),
TRIM(FOODBUY.M7VAGD) AS FBUY_DESCRIPTION,
LEFT(RIGHT(FOODBUY.M7VASD,4),2) || '/' || RIGHT(FOODBUY.M7VASD,2) ||'/' || LEFT(FOODBUY.M7VASD,4) AS FBUY_START,
LEFT(RIGHT(FOODBUY.M7VAED,4),2) || '/' || RIGHT(FOODBUY.M7VAED,2) ||'/' || LEFT(FOODBUY.M7VAED,4) AS FBUY_END,
CAST(DIRECT_VA AS VARCHAR(11)),
TRIM(DIRECT.M7VAGD) AS DIRECT_DESCRIPTION,
LEFT(RIGHT(DIRECT.M7VASD,4),2) || '/' || RIGHT(DIRECT.M7VASD,2) ||'/' || LEFT(DIRECT.M7VASD,4) AS DIRECT_START,
LEFT(RIGHT(DIRECT.M7VAED,4),2) || '/' || RIGHT(DIRECT.M7VAED,2) ||'/' || LEFT(DIRECT.M7VAED,4) AS DIRECT_END,
TRIM(SHIP_TO) AS DCN,
REPLACE(TRIM(CUNAME),'''','') AS CUSTOMER_NAME,
'{timestamp}' AS TIMESTAMP

FROM (

    SELECT DISTINCT
    FOODBUY.LEAD_VA AS FBUY_VA,
    DIRECT.LEAD_VA AS DIRECT_VA,
    CUSTOMER_OVERLAP.SHIP_TO

    FROM (

        SELECT
        M7AGRN AS LEAD_VA,
        M7VAGN AS LOCAL_VA,
        ITEM.SUPC

        FROM (
            SELECT DISTINCT
            CAST(TRIM(BJELEN) AS INT) AS VA

            FROM SCDBFP10.PMFDBJV1

            WHERE BJDPNM LIKE '%FOODBUY%'
            AND LEFT(BJBIE1,2) = 'VA'
            AND UPPER(BJELEN) = LOWER(BJELEN)
            AND BJELEN IS NOT NULL
            AND TRIM(BJELEN) <> ''
        ) AS HEADER

        INNER JOIN SCDBFP10.PMVHM7PF
        ON HEADER.VA = M7AGRN
        AND M7EADT >= {bolw}

        INNER JOIN (
            SELECT
            QBVAGN AS LOCAL_VA,
            QBITEM AS SUPC

            FROM SCDBFP10.PMPZQBPF

            WHERE QBEFED >= {today}
        ) AS ITEM
        ON M7VAGN = ITEM.LOCAL_VA
    ) AS FOODBUY

    INNER JOIN (

        SELECT
        M7AGRN AS LEAD_VA,
        M7VAGN LOCAL_VA,
        ITEM.SUPC

        FROM (
            SELECT DISTINCT
            CAST(TRIM(BJELEN) AS INT) AS VA

            FROM SCDBFP10.PMFDBJV1

            WHERE BJDPNM NOT LIKE '%FOODBUY%'
            AND LEFT(BJBIE1,2) = 'VA'
            AND UPPER(BJELEN) = LOWER(BJELEN)
            AND BJELEN IS NOT NULL
            AND TRIM(BJELEN) <> ''
        ) AS HEADER

        INNER JOIN SCDBFP10.PMVHM7PF
        ON HEADER.VA = M7AGRN
        AND M7EADT >= {bolw}

        INNER JOIN (
            SELECT
            QBVAGN AS LOCAL_VA,
            QBITEM AS SUPC

            FROM SCDBFP10.PMPZQBPF

            WHERE QBEFED >= {today}
        ) AS ITEM
        ON M7VAGN = ITEM.LOCAL_VA
    ) AS DIRECT
    ON FOODBUY.SUPC = DIRECT.SUPC

    INNER JOIN (

        SELECT DISTINCT
        FOODBUY.LEAD_VA AS FOODBUY_VA,
        DIRECT.LEAD_VA AS DIRECT_VA,
        FOODBUY.SHIP_TO

        FROM (

            SELECT DISTINCT
            M7AGRN AS LEAD_VA,
            M7VAGN AS LOCAL_VA,
            CUSTOMER.SHIP_TO

            FROM (
                SELECT DISTINCT
                CAST(TRIM(BJELEN) AS INT) AS VA

                FROM SCDBFP10.PMFDBJV1

                WHERE BJDPNM LIKE '%FOODBUY%'
                AND LEFT(BJBIE1,2) = 'VA'
                AND UPPER(BJELEN) = LOWER(BJELEN)
                AND BJELEN IS NOT NULL
                AND TRIM(BJELEN) <> ''
            ) AS HEADER

            INNER JOIN SCDBFP10.PMVHM7PF
            ON HEADER.VA = M7AGRN
            AND M7EADT >= {bolw}

            INNER JOIN (
                SELECT
                QWVAGN AS LOCAL_VA,
                QWCUNO AS SHIP_TO

                FROM SCDBFP10.PMPZQWPF

                WHERE QWEFED >= {today}
            ) AS CUSTOMER
            ON M7VAGN = CUSTOMER.LOCAL_VA

        ) AS FOODBUY

        INNER JOIN (

            SELECT
            M7AGRN AS LEAD_VA,
            M7VAGN AS LOCAL_VA,
            CUSTOMER.SHIP_TO

            FROM (
                SELECT DISTINCT
                CAST(TRIM(BJELEN) AS INT) AS VA

                FROM SCDBFP10.PMFDBJV1

                WHERE BJDPNM NOT LIKE '%FOODBUY%'
                AND LEFT(BJBIE1,2) = 'VA'
                AND UPPER(BJELEN) = LOWER(BJELEN)
                AND BJELEN IS NOT NULL
                AND TRIM(BJELEN) <> ''
            ) AS HEADER

            INNER JOIN SCDBFP10.PMVHM7PF
            ON HEADER.VA = M7AGRN
            AND M7EADT >={bolw}

            INNER JOIN (
                SELECT
                QWVAGN AS LOCAL_VA,
                QWCUNO AS SHIP_TO

                FROM SCDBFP10.PMPZQWPF

                WHERE QWEFED >= {today}
            ) AS CUSTOMER
            ON M7VAGN = CUSTOMER.LOCAL_VA
        ) AS DIRECT
        ON FOODBUY.SHIP_TO = DIRECT.SHIP_TO
    ) AS CUSTOMER_OVERLAP
    ON FOODBUY.LEAD_VA = CUSTOMER_OVERLAP.FOODBUY_VA
    AND DIRECT.LEAD_VA = CUSTOMER_OVERLAP.DIRECT_VA
)

LEFT JOIN SCDBFP10.PMVHM7PF AS FOODBUY
ON FBUY_VA = FOODBUY.M7AGRN

LEFT JOIN SCDBFP10.PMVHM7PF AS DIRECT
ON DIRECT_VA = DIRECT.M7AGRN

LEFT JOIN ARDBFA.ARPCU
ON SHIP_TO = CUCUNO

LEFT JOIN SCDBFP10.REFERP
ON FOODBUY.M7ARCO = REFKEY
AND REFCAT = 'DM '

WHERE DIRECT.M7VASD <= FOODBUY.M7VAED
AND DIRECT.M7VAED >= FOODBUY.M7VASD
AND FOODBUY.M7AGRN <> 749911
AND DIRECT.M7VAGD NOT LIKE '%REPORTING FEE%'
AND DIRECT.M7VAGD NOT LIKE '%NATIONAL PRICING%'
AND DIRECT.M7VAGD NOT LIKE '%BLANKET%'

ORDER BY
FBUY_VA,
DIRECT_VA,
SHIP_TO
LIMIT 1000
""")

overlap_header_server = F"""
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

overlap_item_server = f"""
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

overlap_customer_server = f"""
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

server_cleanup = """
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
# Server jobs
############################################################################################

cal_backup = (f'''
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
''')