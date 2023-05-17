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