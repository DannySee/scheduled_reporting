
import sql
import test_database_mail
import pandas as pd
import os

cpas_overlaps = {
        (sql.admin_overlaps, f'Overlapping_Admin_Agreements {sql.now}'): [],
        (sql.drop_overlaps, f'Overlapping_Drop_Size_Agreements {sql.now}'): [],
        #(sql.prompt_overlaps, f'overlapping Prompt Pay Agreements {sql.now}'): [],
        (sql.volume_overlaps, f'Overlapping_Volume_Agreements {sql.now}'): [],
        (sql.inco_overlaps, f'Overlapping_Intercompany_Agreements {sql.now}'): [],
        #(sql.edfs_overlaps,  f'overlapping Fuel Surcharge Agreements {sql.now}'): [],
        (sql.licg_overlaps, f'Overlapping_Upcharge_Agreements {sql.now}'): [],
        (sql.charge_overlaps, f'Overlapping_Surcharge_Agreements {sql.now}'): []
    }

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

        test_database_mail.send_message(filepath)

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

        test_database_mail.send_message(filename)

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

        test_database_mail.send_message(filename)

        os.remove(filename)

