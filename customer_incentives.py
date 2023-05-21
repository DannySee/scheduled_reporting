
import date_formats as dt
import sql

############################################################################################
# Weekly Overlapping Agreements Reports
############################################################################################

admin_overlaps = {
    'sql': sql.admin_overlaps, 
    'filename': f'Overlapping_Admin_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Admin Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\n\nOverlapping Admin Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
} 

drop_overlaps = {
    'sql': sql.drop_overlaps, 
    'filename': f'Overlapping_Drop_Size_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Drop Size Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\n\nOverlapping Drop Size Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

prompt_overlaps = {
    'sql': sql.prompt_overlaps, 
    'filename': f'Overlapping_Prompt_Pay_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Prompt Pay Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\n\nOverlapping Prompt Pay Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

volume_overlaps  = {
    'sql': sql.volume_overlaps, 
    'filename': f'Overlapping_Volume_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Volume Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\n\nOverlapping Volume Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

inco_overlaps = {
    'sql': sql.inco_overlaps, 
    'filename': f'Overlapping_Intercompany_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping INCO Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\n\nOverlapping INCO Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

edfs_overlaps = {
    'sql': sql.edfs_overlaps, 
    'filename': f'overlapping_Fuel_Surcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CI) Overlapping Fule Surcharge Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\n\nOverlapping Fuel Surcharge Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

licg_overlaps = {
    'sql': sql.licg_overlaps, 
    'filename': f'Overlapping_Upcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CIR) Overlapping LICG Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\n\nOverlapping LICG Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

charge_overlaps = {
    'sql': sql.charge_overlaps, 
    'filename': f'Overlapping_Surcharge_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '',
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'(CIR) Overlapping Charge/Surcharge Agreements: Week of {dt.pretty("beginning_of_last_week")}',
    'mail_body': f'Customer Incentives & Rebates:\n\nOverlapping Charge/Surcharge Agreements {dt.pretty("beginning_of_last_week")} to {dt.pretty("end_of_last_week")}.'
}

############################################################################################
# Dailiy UPDL Validation Report
############################################################################################

updl_violation = {
    'sql': sql.updl_violation, 
    'filename': f'UPDL_DL_Violation_{dt.pretty("today")}',
    'data': [], 
    'headers': '', 
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'UPDL Agreement Rebate Basis Violation {dt.pretty("today")}',
    'mail_body': f"The attached UPDL agreement(s) are setup with a rebate basis other than DL. Please review and take the appropriate action.\n\n\nThanks,\nQA Pricing & Agreements"  
}

############################################################################################
# Monthly Expiring Deals Report
############################################################################################

expiring_deals = {
    'sql': sql.expiring_deals, 
    'filename': f'Expiring_CI_Agreements_{dt.pretty("today")}',
    'data': [], 
    'headers': '', 
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'Expiring Performance Agreements {dt.pretty("today")}',
    'mail_body': f"The attached performance agreemenet(s) are set to expire this month."  
}

############################################################################################
# Monthly Expiring Deals Report
############################################################################################

daily_validation = {
    'sql': sql.daily_ci_validation, 
    'filename': f'Daily_Performance_Agreement_Validation_{dt.pretty("today")}',
    'data': [], 
    'headers': '', 
    'mail_to': 'daniel.clark@sysco.com',
    'mail_subject': f'Daily Performance Agreement Validation {dt.pretty("today")}',
    'mail_body': f'Daily performance agreement validation - agreement(s) created/modified {dt.pretty("yesterday")}.'
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