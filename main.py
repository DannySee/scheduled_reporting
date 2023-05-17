from data_pull import pull_usbl
from customer_incentives import ci_overlaps
import sql

daily_jobs = sql.cal_backup


if __name__ == "__main__":

    

    #cpas.updl_validation()
    #cpas.overlaps()
    #mail.send_message()
    #cpas.expiring_deals()

    pull_usbl(ci_overlaps)
    s