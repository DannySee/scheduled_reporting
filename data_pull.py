import os
import data_centers as cnn

from excel import create_file
from database_mail import send_message
from deviated_agreements import upload_foodbuy_overlaps


def pull_usbl(reports):

    sites = cnn.all_sites
    #sites = ['058']s
 
    for site in sites:
        try:
            sus = cnn.sus(site)
            cur = sus.cursor()

            for report in reports:

                if 'custom_job' in report:

                    report['custom_job']['import'](sus)
            
                else:

                    # insert market details if applicable
                    query = report['sql'].replace('*MARKET*', cnn.site_markets[site])

                    # fetch data from system
                    cur.execute(query)
                    query_results = cur.fetchall()

                    # extend data site for query/site
                    report['data'].extend([list(map(str, row)) for row in query_results])

                    # setup the headers for each report
                    report['headers'] = [desc[0] for desc in cur.description]
                
            sus.close()
            print(f'(USBL) Data Pull Complete: {site}')

        except Exception as e:
            print(f'(USBL) Cannot connect to site ({site})\n{e}')

    for report in reports:

        filename = f"C:\\Temp\\outgoing_mail\\{report['filename']}.xlsx"
        headers = report['headers']
        content = report['data']
        mail_to = report['mail_to']
        mail_subject = report['mail_subject']
        mail_body = f'{report["mail_body"]}\n\nRecord count: {len(report["data"])}'

        if 'custom_job' in report:
            report['custom_job']['export']
        else:
            create_file(filename, headers, content)

        send_message(mail_to, mail_subject, mail_body, filename)

        os.remove(filename)

