import date_formats as dt
import server_jobs
import customer_incentives as ci

from data_pull import pull_usbl


if __name__ == "__main__":

    # daily jobs
    server_jobs.cal_backup

    # daily reporting
    sus_reporting = [ci.updl_violation]

    # weekly reporting
    if dt.now.weekday() == 0:
        sus_reporting.extend(ci.overlaps)

    # monthly reporting
    if dt.now.day() == 1:
        sus_reporting.append(ci.expiring_deals)

    # run reporting accross usbl
    pull_usbl(sus_reporting)
    