import deviated_agreements as dpm
import customer_incentives as ci

from data_pull import sus_reporting
from data_centers import all_sites


if __name__ == "__main__":

    sus_reporting([dpm.rebate_basis_validatoin], ['240'])
    sus_reporting([ci.updl_violation], all_sites)