import data_centers


def pull_usbl():

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
