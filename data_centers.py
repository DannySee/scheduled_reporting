import pyodbc

# sql server connection properties
sql_server = pyodbc.connect(
    driver='{SQL Server}',
    server='MS248CSSQL01.SYSCO.NET',
    database='Pricing_Agreements')

# dictionary of all opsites 3 (key=3 digit number, value=3 digit number + name)
site_names = {
    '001': '001 - Jackson',
    '002': '002 - Atlanta',
    '003': '003 - Jacksonville',
    '004': '004 - Central California (Modesto)',
    '005': '005 - Intermountain (UT)',
    '006': '006 - Dallas (North Texas)',
    '007': '007 - Virginia',
    '008': '008 - Northern New England',
    '009': '009 - Pittsburgh',
    '010': '010 - East Maryland (Lankford)',
    '011': '011 - Lousiville',
    '012': '012 - Baltimore (Smelkinson)',
    '013': '013 - Central TX (San Antonio & Austin)',
    '014': '014 - Memphis (Hardins)',
    '015': '015 - Cleveland',
    '016': '016 - South Florida (Miami)(Medley)',
    '017': '017 - Las Vegas',
    '018': '018 - Baraboo (Winsconsin)',
    '019': '019 - Cincinnati',
    '022': '022 - Central Florida (Ocoee)',
    '023': '023 - New Orleans',
    '024': '024 - Chicago',
    '025': '025 - Albany',
    '026': '026 - Oklahoma',
    '027': '027 - Syracuse',
    '029': '029 - Arkansas',
    '031': '031 - Sacramento',
    '032': '032 - S.E. Florida',
    '035': '035 - East Wisconsin',
    '036': '036 - San Diego',
    '037': '037 - West Coast Florida (Palmetto)',
    '038': '038 - Indianapolis',
    '039': '039 - Iowa',
    '040': '040 - Idaho',
    '043': '043 - Montana',
    '045': '045 - Los Angeles',
    '046': '046 - Central Alabama (Birmingham)',
    '047': '047 - Minnesota',
    '048': '048 - Charlotte',
    '049': '049 - Arizona',
    '050': '050 - San Francisco',
    '051': '051 - Central PA',
    '052': '052 - Portland',
    '054': '054 - Connecticut',
    '055': '055 - Seattle (Washington)',
    '056': '056 - Boston (Hallsmith)',
    '057': '057 - Kansas City',
    '058': '058 - Detroit',
    '059': '059 - Denver',
    '060': '060 - Nashville (Robert Orr)',
    '061': '061 - Nebraska (Lincoln)(Pegler) ',
    '064': '064 - St. Louis',
    '066': '066 - New Mexico  (Nobel) ',
    '067': '067 - Houston',
    '068': '068 - Grand Rapids',
    '073': '073 - Hampton Roads (VA)',
    '075': '075 - Philadelphia',
    '076': '076 - Metro New York',
    '078': '078 - West Texas (Watson)(Lubbock)',
    '101': '101 - Ventura',
    '102': '102 - Spokane',
    '134': '134 - Intl Food Group (IFG)-Tampa',
    '137': '137 - Columbia',
    '163': '163 - Raleigh',
    '164': '164 - Gulf Coast',
    '194': '194 - Central Illinois (Roberts)',
    '195': '195 - North Dakota',
    '240': '240 - Corporate',
    '288': '288 - Knoxville',
    '293': '293 - East Texas',
    '306': '306 - Long Island',
    '320': '320 - Riverside',
    '332': '332 - Western Minnesota',
    '344': '344 - Intl Food Group (IFG)-Jacksonville',
    '429': '429 - Doerle',
    '450': '450 - Alaska (NO DPM)'
}

# dictionary of all opsites 3 (key=3 digit number, value=3 digit number + name)
site_markets = {
    '001': 'South Market',
    '002': 'South Market',
    '003': 'South Market',
    '004': 'West Market',
    '005': 'West Market',
    '006': 'South Market',
    '007': 'North Market',
    '008': 'North Market',
    '009': 'North Market',
    '010': 'South Market',
    '011': 'North Market',
    '012': 'North Market',
    '013': 'South Market',
    '014': 'South Market',
    '015': 'North Market',
    '016': 'South Market',
    '017': 'West Market',
    '018': 'North Market',
    '019': 'North Market',
    '022': 'South Market',
    '023': 'South Market',
    '024': 'North Market',
    '025': 'North Market',
    '026': 'South Market',
    '027': 'North Market',
    '029': 'South Market',
    '031': 'West Market',
    '032': 'South Market',
    '035': 'North Market',
    '036': 'West Market',
    '037': 'South Market',
    '038': 'North Market',
    '039': 'North Market',
    '040': 'West Market',
    '043': 'West Market',
    '045': 'West Market',
    '046': 'South Market',
    '047': 'North Market',
    '048': 'South Market',
    '049': 'West Market',
    '050': 'West Market',
    '051': 'North Market',
    '052': 'West Market',
    '054': 'North Market',
    '055': 'West Market',
    '056': 'North Market',
    '057': 'West Market',
    '058': 'North Market',
    '059': 'West Market',
    '060': 'South Market',
    '061': 'West Market',
    '064': 'North Market',
    '066': 'West Market',
    '067': 'South Market',
    '068': 'North Market',
    '073': 'South Market',
    '075': 'North Market',
    '076': 'North Market',
    '078': 'South Market',
    '101': 'West Market',
    '102': 'West Market',
    '137': 'South Market',
    '163': 'South Market',
    '164': 'South Market',
    '194': 'North Market',
    '195': 'North Market',
    '288': 'South Market',
    '293': 'South Market',
    '306': 'North Market',
    '320': 'West Market',
    '332': 'North Market',
    '429': 'South Market', 
    '450': 'West Market'
}

# list of all north market sites (3 digit numbers)
north_market = ['007', '008', '009', '011', '012', '015', '018', '019', '024', '025', '027', '035', '038', '039', '047',
                '051', '054',
                '056', '058', '064', '068', '075', '076', '194', '195', '306', '332']

# list of all south market sites (3 digit numbers)
south_market = ['001', '002', '003', '006', '010', '013', '014', '016', '022', '023', '026', '029', '032', '037', '046',
                '048', '060',
                '067', '073', '078', '137', '163', '164', '288', '293', '429']

# list of all west market sites (3 digit numbers)
west_market = ['004', '005', '017', '031', '036', '040', '043', '045', '049', '050', '052', '055', '057', '059', '061',
               '066', '101',
               '102', '320', '450']

# list of all sites using the keys of all sites dictionary
all_sites = site_names.keys()


# function to establish connection to sus and return sus object
def sus(site):
    cnn_sus = pyodbc.connect(
        driver='{iSeries Access ODBC Driver}',
        system=f'AS{site}ATO.na.sysco.net',
        SIGNON=4,
        TRANSLATE=1,
        TRANSLATE_BINARY=True)

    return cnn_sus


for site in west_market:
    print(f"'{site}': 'West Market',")