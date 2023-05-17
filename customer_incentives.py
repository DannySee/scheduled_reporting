
import sql
import date_formats as dt

admin_overlaps = {
    'sql': sql.admin_overlaps, 
    'filename': f'Overlapping_Admin_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Admin Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping Admin Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
} 

drop_overlaps = {
    'sql': sql.drop_overlaps, 
    'filename': f'Overlapping_Drop_Size_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Drop Size Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping Drop Size Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

prompt_overlaps = {
    'sql': sql.prompt_overlaps, 
    'filename': f'Overlapping_Prompt_Pay_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Prompt Pay Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping Prompt Pay Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

volume_overlaps  = {
    'sql': sql.volume_overlaps, 
    'filename': f'Overlapping_Volume_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Volume Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping Volume Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

inco_overlaps = {
    'sql': sql.inco_overlaps, 
    'filename': f'Overlapping_Intercompany_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping INCO Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping INCO Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

edfs_overlaps = {
    'sql': sql.edfs_overlaps, 
    'filename': f'overlapping_Fuel_Surcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Fule Surcharge Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping Fuel Surcharge Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

licg_overlaps = {
    'sql': sql.licg_overlaps, 
    'filename': f'Overlapping_Upcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping LICG Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping LICG Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

charge_overlaps = {
    'sql': sql.charge_overlaps, 
    'filename': f'Overlapping_Surcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Charge/Surcharge Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives: Overlapping Charge/Surcharge Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

ci_overlaps = [admin_overlaps, drop_overlaps, volume_overlaps, inco_overlaps, licg_overlaps, charge_overlaps]
       
        
        

'''
def updl_validation():

    sites = data_centers.all_sites
    violations = []

    for site in sites:
        sus = data_centers.sus(site)
        query = sus.execute(sql.updl_dl_violation).fetchall()

        for row in query:
            rowList = [
                str(row.SITE),
                str(row.CA) ,
                str(row.DESCRIPTION) ,
                str(row.START_DT),
                str(row.END_DT)
            ]
            violations.append(rowList)
            
        print(f'UPDL {site}')
        sus.close()

    if len(violations) > 0:

        filename = 'UPDL Rebate Basis Violation.xlsx'

        df = pd.DataFrame(violations, columns=["SITE", "CA", "DESCRIPTION", "START", "END"])
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

        filepath = os.getcwd() + f'\{filename}'

        to = "corporatecustomerrebates@sbs.sysco.com"
        subject = "UPDL Agreement Rebate Basis Violation"
        body = f"Good afternoon,\n\nThe attached UPDL agreements are setup with a rebate basis other than DL. Please review and take the appropriate action.\n\n\nThanks,\nQA Pricing & Agreements"    

        database_mail.send_message(filepath)

        os.remove(filepath)


def overlaps():

    sites = data_centers.all_sites
    

    for site in sites:

        try:
            sus = data_centers.sus(site)
            print(site)

            for query in cpas_overlaps:

                print('new type')

                query_results = sus.execute(query[0]).fetchall()

                for row in query_results:
                    rows = [
                        row.SITE, 
                        row.PRNT_LEAD_CA,
                        row.PRNT_LOCAL_CA, 
                        row.PRNT_DESCRIPTION,
                        row.PRNT_START, 
                        row.PRNT_END,
                        row.CHLD_LEAD_CA, 
                        row.CHLD_LOCAL_CA,
                        row.CHLD_DESCRIPTION, 
                        row.CHLD_START, 
                        row.CHLD_END
                    ]
                    cpas_overlaps[query].append(rows)
        except:
            print(f'could not gain access to site ({site}).')

    i = 1
    for report in cpas_overlaps:

        filename = f'C:\\Temp\\outgoing_mail\\{report[1]}.xlsx'

        df = pd.DataFrame(cpas_overlaps[report], columns=["SITE", "LEAD CA", "LOCAL CA","DESCRIPTION","START","END","LEAD CA", "LOCAL CA","DESCRIPTION","START","END"])
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer, sheet_name=sql.today, index=False)

        i = i + 1 

        database_mail.send_message(filename)

        os.remove(filename)


def expiring_deals():

    sites = data_centers.all_sites
    usbl_results = []

    for site in sites:
        try:
            sus = data_centers.sus(site)
            cur = sus.cursor()
            cur.execute(sql.expiring_deals)
            site_results = cur.fetchall()

            headers = [desc[0] for desc in cur.description]
            usbl_results.extend([list(map(str, row)) for row in site_results])
                
            sus.close()
            print(f'Expiring: {site}')
        except Exception as e:
            print(f'Cannot connect to site ({site})\n{e}')

    if len(usbl_results) > 0:

        filename = f'C:\\Temp\\outgoing_mail\\CPAS Expiring Deals Report {sql.now}.xlsx'

        df = pd.DataFrame(usbl_results, columns=headers)
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer, sheet_name='sheet1', index=False)

        to = "corporatecustomerrebates@sbs.sysco.com"
        subject = "UPDL Agreement Rebate Basis Violation"
        body = f"Good afternoon,\n\nThe attached UPDL agreements are setup with a rebate basis other than DL. Please review and take the appropriate action.\n\n\nThanks,\nQA Pricing & Agreements"    

        database_mail.send_message(filename)

        

'''