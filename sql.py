from datetime import  datetime, timedelta, date
import date_formats as dt

now = date.today()
today = now.strftime('%Y%m%d')
yesterday = (now - timedelta(1)).strftime('%Y%m%d')
last_week_start = (now - timedelta(days=now.weekday()+8)).strftime('%Y%m%d')
last_week_end = (now - timedelta(days=now.weekday()+2)).strftime('%Y%m%d')
next_month = now.replace(day=28) + timedelta(days=4)
end_of_month = (next_month - timedelta(days=next_month.day)).strftime('%Y%m%d')
beginning_of_month = (datetime(now.year, now.month, 1)).strftime('%Y%m%d')

updl_dl_violation = (f'''
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

    WHERE NHEADT = {dt.sus_format("yesterday")}
    AND NHAGTY = 'UPDL' 
    AND NHPFRB <> 'DL'
    AND NHAGRN = 0   
''')

inco_overlaps = (f'''
    SELECT DISTINCT
    T1.NHARCO AS SITE, 
    'MARKET' AS MARKET,
    T1.NHAGRN AS PRNT_LEAD_CA,
    T1.NHCANO AS PRNT_LOCAL_CA, 
    TRIM(T1.NHCADC) AS PRNT_DESCRIPTION,
    T1.NHCASD AS PRNT_START, 
    T1.NHCAED AS PRNT_END,
    T2.NHAGRN AS CHLD_LEAD_CA,
    T2.NHCANO AS CHLD_LOCAL_CA, 
    TRIM(T2.NHCADC) AS CHLD_DESCRIPTION,
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
        T1.NHEADT BETWEEN {dt.sus_format("beginning_of_last_week")} AND {last_week_end} 
        OR T1.NHMODT BETWEEN {dt.sus_format("beginning_of_last_week")} AND {last_week_end} 
    )
    AND T1.NHCAED >= {today}
    AND T2.NHCAED >= {today}
    AND T1.NHAGTY = 'INCO'
''')

admin_overlaps = (f'''
    SELECT DISTINCT
    T1.NHARCO AS SITE, 
    'MARKET' AS MARKET,
    T1.NHAGRN AS PRNT_LEAD_CA,
    T1.NHCANO AS PRNT_LOCAL_CA, 
    TRIM(T1.NHCADC) AS PRNT_DESCRIPTION,
    T1.NHCASD AS PRNT_START, 
    T1.NHCAED AS PRNT_END,
    T2.NHAGRN AS CHLD_LEAD_CA,
    T2.NHCANO AS CHLD_LOCAL_CA, 
    TRIM(T2.NHCADC) AS CHLD_DESCRIPTION,
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
        T1.NHEADT BETWEEN {last_week_start} AND {last_week_end} 
        OR T1.NHMODT BETWEEN {last_week_start} AND {last_week_end} 
    )
    AND T1.NHCAED >= {today}
    AND T2.NHCAED >= {today}
    AND T1.NHAGTY IN (
        'ASR1',
        'ASR2',
        'ASR3',
        'ASR4'
    )
''')


drop_overlaps = (f'''
    SELECT DISTINCT
    T1.NHARCO AS SITE, 
    'MARKET' AS MARKET,
    T1.NHAGRN AS PRNT_LEAD_CA,
    T1.NHCANO AS PRNT_LOCAL_CA, 
    TRIM(T1.NHCADC) AS PRNT_DESCRIPTION,
    T1.NHCASD AS PRNT_START, 
    T1.NHCAED AS PRNT_END,
    T2.NHAGRN AS CHLD_LEAD_CA,
    T2.NHCANO AS CHLD_LOCAL_CA, 
    TRIM(T2.NHCADC) AS CHLD_DESCRIPTION,
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
        T1.NHEADT BETWEEN {last_week_start} AND {last_week_end} 
        OR T1.NHMODT BETWEEN {last_week_start} AND {last_week_end} 
    )
    AND T1.NHCAED >= {today}
    AND T2.NHCAED >= {today}
    AND T1.NHAGTY IN (
        'DPI1',
        'DPI2',
        'DPI3',
        'DPI4',
        'DPI5',
        'DPI6',
        'DPA1',
        'DPA2',
        'DPA3',
        'DPA4',
        'DRUP',
        'EDCP'
    )
''')

volume_overlaps = (f'''
    SELECT DISTINCT
    T1.NHARCO AS SITE, 
    'MARKET' AS MARKET,
    T1.NHAGRN AS PRNT_LEAD_CA,
    T1.NHCANO AS PRNT_LOCAL_CA, 
    TRIM(T1.NHCADC) AS PRNT_DESCRIPTION,
    T1.NHCASD AS PRNT_START, 
    T1.NHCAED AS PRNT_END,
    T2.NHAGRN AS CHLD_LEAD_CA,
    T2.NHCANO AS CHLD_LOCAL_CA, 
    TRIM(T2.NHCADC) AS CHLD_DESCRIPTION,
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
        T1.NHEADT BETWEEN {last_week_start} AND {last_week_end} 
        OR T1.NHMODT BETWEEN {last_week_start} AND {last_week_end} 
    )
    AND T1.NHCAED >= {today}
    AND T2.NHCAED >= {today}
    AND T1.NHAGTY IN (
        'BDS1',
        'BDS2',
        'BDS3',
        'BDS4',
        'BDV1',
        'BDV2',
        'BDV3',
        'BDV4',
        'BDV5',
        'BDV6',
        'BDV7',
        'BDV8',
        'VPR1',
        'VPR2',
        'VPR3',
        'VPR4',
        'VPR5',
        'VPR6',
        'VPR7',
        'VPR8'
    )
''')

licg_overlaps = (f'''
    SELECT DISTINCT
    T1.NHARCO AS SITE, 
    'MARKET' AS MARKET,
    T1.NHAGRN AS PRNT_LEAD_CA,
    T1.NHCANO AS PRNT_LOCAL_CA, 
    TRIM(T1.NHCADC) AS PRNT_DESCRIPTION,
    T1.NHCASD AS PRNT_START, 
    T1.NHCAED AS PRNT_END,
    T2.NHAGRN AS CHLD_LEAD_CA,
    T2.NHCANO AS CHLD_LOCAL_CA, 
    TRIM(T2.NHCADC) AS CHLD_DESCRIPTION,
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
        T1.NHEADT BETWEEN {last_week_start} AND {last_week_end} 
        OR T1.NHMODT BETWEEN {last_week_start} AND {last_week_end} 
    )
    AND T1.NHCAED >= {today}
    AND T2.NHCAED >= {today}
    AND T1.NHAGTY = 'LICG'
''')

charge_overlaps = (f'''
    SELECT DISTINCT
    T1.NHARCO AS SITE, 
    'MARKET' AS MARKET,
    T1.NHAGRN AS PRNT_LEAD_CA,
    T1.NHCANO AS PRNT_LOCAL_CA, 
    TRIM(T1.NHCADC) AS PRNT_DESCRIPTION,
    T1.NHCASD AS PRNT_START, 
    T1.NHCAED AS PRNT_END,
    T2.NHAGRN AS CHLD_LEAD_CA,
    T2.NHCANO AS CHLD_LOCAL_CA, 
    TRIM(T2.NHCADC) AS CHLD_DESCRIPTION,
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
        T1.NHEADT BETWEEN {last_week_start} AND {last_week_end} 
        OR T1.NHMODT BETWEEN {last_week_start} AND {last_week_end} 
    )
    AND T1.NHCAED >= {today}
    AND T2.NHCAED >= {today}
    AND T1.NHAGTY IN (
        'UPCH',
        'LASU'
    )
''')

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
    AND NHCAED BETWEEN {beginning_of_month} AND {end_of_month}
''')