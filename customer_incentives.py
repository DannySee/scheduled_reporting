
import date_formats as dt
import sql

############################################################################################
# Weekly Overlapping Agreements Reports
############################################################################################

admin_overlaps = {
    'sql': sql.admin_overlaps, 
    'send_if_null': True,
    'filename': f'Overlapping_Admin_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'(CIR) Overlapping Admin Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\nOverlapping Admin Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
} 

drop_overlaps = {
    'sql': sql.drop_overlaps, 
    'send_if_null': True,
    'filename': f'Overlapping_Drop_Size_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'(CIR) Overlapping Drop Size Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\nOverlapping Drop Size Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

prompt_overlaps = {
    'sql': sql.prompt_overlaps, 
    'send_if_null': True,
    'filename': f'Overlapping_Prompt_Pay_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'(CIR) Overlapping Prompt Pay Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\nOverlapping Prompt Pay Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

volume_overlaps  = {
    'sql': sql.volume_overlaps, 
    'send_if_null': True,
    'filename': f'Overlapping_Volume_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'(CIR) Overlapping Volume Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\nOverlapping Volume Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

inco_overlaps = {
    'sql': sql.inco_overlaps, 
    'send_if_null': True,
    'filename': f'Overlapping_Intercompany_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'(CIR) Overlapping INCO Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\nOverlapping INCO Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

edfs_overlaps = {
    'sql': sql.edfs_overlaps, 
    'send_if_null': True,
    'filename': f'overlapping_Fuel_Surcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'(CIR) Overlapping Fule Surcharge Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\nOverlapping Fuel Surcharge Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

licg_overlaps = {
    'sql': sql.licg_overlaps, 
    'send_if_null': True,
    'filename': f'Overlapping_Upcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'(CIR) Overlapping LICG Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\nOverlapping LICG Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

charge_overlaps = {
    'sql': sql.charge_overlaps, 
    'send_if_null': True,
    'filename': f'Overlapping_Surcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'qapricingagreements@sbs.sysco.com',
    'mail_subject': f'(CIR) Overlapping Charge/Surcharge Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\nOverlapping Charge/Surcharge Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

############################################################################################
# Dailiy UPDL Validation Report
############################################################################################

updl_violation = {
    'sql': sql.updl_violation, 
    'send_if_null': False,
    'filename': f'UPDL_DL_Violation_{dt.pretty("today")}',
    'data': [], 
    'headers': '', 
    'mail_to': 'rachel.adams@sysco.com;cheri.otto@sysco.com;julie.samuel@sysco.com',
    'mail_subject': f'UPDL Agreement Rebate Basis Violation {dt.pretty("today")}',
    'mail_body': f"The attached UPDL agreement(s) are setup with a rebate basis other than DL."  
}

############################################################################################
# Monthly Expiring Deals Report
############################################################################################

expiring_deals = {
    'sql': sql.expiring_deals, 
    'send_if_null': True,
    'filename': f'Expiring_CI_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '', 
    'mail_to': 'rachel.adams@sysco.com',
    'mail_subject': f'Expiring Performance Agreements {dt.pretty("today")}',
    'mail_body': f"The attached performance agreemenet(s) are set to expire this month."  
}

############################################################################################
# Daily validation report
############################################################################################

daily_validation = {
    'sql': sql.daily_ci_validation, 
    'send_if_null': True,
    'filename': f'Daily_Performance_Agreement_Validation_{dt.pretty("today")}',
    'data': [], 
    'headers': '', 
    'mail_to': 'rachel.adams@sysco.com;cheri.otto@sysco.com;julie.samuel@sysco.com;michelle.graves@sysco.com',
    'mail_subject': f'Daily Performance Agreement Validation {dt.pretty("today")}',
    'mail_body': f'Daily Performance Agreement Validation:\nAgreement(s) created/modified {dt.pretty("yesterday")}.'
}

############################################################################################
# Reporting Clusters
############################################################################################

overlaps = [
    admin_overlaps, 
    drop_overlaps, 
    volume_overlaps,
    inco_overlaps,
    licg_overlaps,
    charge_overlaps
]

all_reports = [
    admin_overlaps, 
    drop_overlaps, 
    volume_overlaps, 
    inco_overlaps, 
    licg_overlaps, 
    charge_overlaps, 
    updl_violation, 
    expiring_deals,
    daily_validation
]