import date_formats as dt
import server_jobs
import customer_incentives as ci
import deviated_agreements as dpm

from data_pull import sus_reporting
from data_centers import all_sites


if __name__ == "__main__":

    # daily jobs
    server_jobs.cal_backup()

    # daily reporting
    report_list = [ci.daily_validation]

    # weekly reporting
    if dt.now.weekday() == 0:
        report_list.extend(ci.overlaps)
        report_list.append(dpm.foodbuy_overlaps)

    # monthly reporting
    if dt.now.day == 1:
        report_list.append(ci.expiring_deals)

    # run reporting accross usbl
    sus_reporting(report_list, all_sites)

