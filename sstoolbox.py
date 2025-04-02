import pandas as pd
import numpy as np
from datetime import datetime

primaryColorRGB   = "rgba(193, 110, 112, 1)"
primaryColorRGBA  = "rgba(193, 110, 112, 0.6)"
primaryColor      = "#C16E70"
backgroundColor   = "#FFFFFF"
secondaryBackgroundColor ="#F2F4F3"
textColor         = "#030027"
textColor         = "#151E3F"
colorGreen        = '#508484'
colorOrange       = '#CBA135'
colorRed          = '#C16E70'
colorGray         = '#6B7D7D'
colorTurquoise    = '#28AFB0'
colorYellowGreen  = '#95C623'
colorMidGray      = '#5D737E'
colorLightPink    = '#FFE5D4'

dictStatement = {
  "R&D" : "Research Development",
  "GrossProfit" : "Gross Profit"
}

# Define data to scrape
# NASDAQ Datalink
dictNDDL = {
"FOMC_FedFundsRate_High":       {'key': 'FRED/FEDTARRH',                        'frequency': 'yearly', 'category': 'Rate', 'description':''},
"FOMC_FedFundsRate_Mid":        {'key': 'FRED/FEDTARRM',                        'frequency': 'yearly', 'category': 'Rate', 'description':''},
"FOMC_FedFundsRate_Low":        {'key': 'FRED/FEDTARRL',                        'frequency': 'yearly', 'category': 'Rate', 'description':''},
"Shiller PE Ratio":             {'key': 'MULTPL/SHILLER_PE_RATIO_MONTH',        'frequency': 'monthly', 'category': 'SP500', 'description':''},
"S&P500 PE Ratio":              {'key': 'MULTPL/SP500_PE_RATIO_MONTH',          'frequency': 'monthly', 'category': 'SP500', 'description':''},
"S&P500 Earnings Yield":        {'key': 'MULTPL/SP500_EARNINGS_YIELD_MONTH',    'frequency': 'monthly', 'category': 'SP500', 'description':''},
"S&P 500 Dividend Yield":       {'key': 'MULTPL/SP500_DIV_YIELD_MONTH',         'frequency': 'monthly', 'category': 'SP500', 'description':''},
"S&P 500 Real Price":           {'key': 'MULTPL/SP500_REAL_PRICE_MONTH',        'frequency': 'monthly', 'category': 'SP500', 'description':''},
"S&P 500 Inflation Adjusted":   {'key': 'MULTPL/SP500_INFLADJ_MONTH',           'frequency': 'monthly', 'category': 'SP500', 'description':''},
"Strategic Petroleum Reserve":  {'key': 'EIA/STEO_COSQPUS_M',                   'frequency': 'monthly', 'category': 'Commodity', 'description':''},
"Retail Trading":               {'key': 'NDAQ/RTAT10',                          'frequency': 'daily', 'category': 'Ticker', 'description':''},
}
# Alpha Vantage
dictAlphaVantage = {
"FedFundsRate":                 {'key': 'FEDERAL_FUNDS_RATE',         'frequency': 'daily', 'category': 'Rate', 'description':''},
"Real GDP":                     {'key': 'REAL_GDP',                   'frequency': 'quarterly', 'category': '', 'description':''},
"CPI":                          {'key': 'REAL_GDP_PER_CAPITA',        'frequency': 'monthly', 'category': 'Econ', 'description':''},
"Inflation Expection":          {'key': 'INFLATION_EXPECTATION',      'frequency': 'monthly', 'category': '', 'description':''},
"Consumer Sentiment":           {'key': 'CONSUMER_SENTIMENT',         'frequency': 'monthly', 'category': '', 'description':''},
"Retail Sales":                 {'key': 'RETAIL_SALES',               'frequency': 'monthly', 'category': '', 'description':''},
"Durables":                     {'key': 'DURABLES',                   'frequency': 'monthly', 'category': '', 'description':''},
"Unemployment":                 {'key': 'UNEMPLOYMENT',               'frequency': 'monthly', 'category': '', 'description':''},
"Nonfarm Payroll":              {'key': 'NONFARM_PAYROLL',            'frequency': 'monthly', 'category': '', 'description':''},
}
# Yahoo Finance
dictDataInfoParams = {
  # Original Parameters
  'twitter'                       : {'keep': True,  'keepAnalysisPg': True , 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'twitter',         'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'zip'                           : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'zip',             'dType': 'int' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'sector'                        : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'sector',          'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fullTimeEmployees'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Employee',        'dType': 'int' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'longBusinessSummary'           : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'summary',         'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'city'                          : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'city',            'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'phone'                         : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'phone',           'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'state'                         : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'state',           'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'country'                       : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'country',         'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'companyOfficers'               : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'companyOfficers', 'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'website'                       : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'website',         'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'maxAge'                        : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'maxAge',          'dType': 'int' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'address1'                      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'address',         'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'industry'                      : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'industry',        'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'ebitdaMargins'                 : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'EBIDAMargins',    'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1,    'plotMax': 1, 'dbName': '', 'description': '' }, 
  'profitMargins'                 : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 17,   'shortName': 'Profit Margins',   'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1,    'plotMax': 1, 'dbName': '', 'description': '' }, 
  'profitMargins_(pct)'           : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'calc',   'idxAnalysisPg': 17,   'shortName': 'Profit Margins (%)',   'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1,    'plotMax': 1, 'dbName': '', 'description': '' }, 
  'grossMargins'                  : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 15,   'shortName': 'Gross Margins',    'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1,    'plotMax': 1, 'dbName': '', 'description': '' }, 
  'grossMargins_(pct)'            : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'calc',   'idxAnalysisPg': 15,   'shortName': 'Gross Margins (%)',    'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1,    'plotMax': 1, 'dbName': '', 'description': '' }, 
  'operatingCashflow'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'OperatingCF',     'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': np.nan,'plotMax': np.nan, 'dbName': '', 'description': '' }, 
  'revenueGrowth'                 : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 18,   'shortName': 'Revenue Growth',   'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1,    'plotMax': np.nan, 'dbName': '', 'description': '' }, 
  'revenueGrowth_(pct)'           : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'calc',   'idxAnalysisPg': 18,   'shortName': 'Revenue Growth (%)',   'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1,    'plotMax': np.nan, 'dbName': '', 'description': '' }, 
  'operatingMargins'              : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 16,   'shortName': 'OperatingMargins','dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1,    'plotMax': 1, 'dbName': '', 'description': '' }, 
  'ebitda'                        : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'EBITDA',          'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': np.nan,'plotMax': np.nan, 'dbName': '', 'description': '' }, 
  'targetLowPrice'                : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Target Low Price ($)',        'dType': 'int' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'targetLow_(pct)'               : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': None, 'shortName': 'Target Low (%)',        'dType': 'int' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'recommendationKey'             : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Recommendation',  'dType': 'str' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'grossProfits'                  : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': 3,    'shortName': 'Gross Profits',    'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': np.nan,'plotMax': np.nan, 'dbName': '', 'description': '' }, 
  'grossProfits_(B)'              : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': 3,    'shortName': 'Gross Profits (B)',    'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': np.nan,'plotMax': np.nan, 'dbName': '', 'description': '' }, 
  'freeCashflow'                  : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': 4,    'shortName': 'FCF',             'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': np.nan,'plotMax': np.nan, 'dbName': '', 'description': '' }, 
  'freeCashflow_(B)'              : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': 4,    'shortName': 'FCF (B)',             'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': np.nan,'plotMax': np.nan, 'dbName': '', 'description': '' }, 
  'targetMedianPrice'             : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Target Median Price ($)',     'dType': 'int' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'targetMedian_(pct)'            : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': None, 'shortName': 'Target Median (%)',     'dType': 'int' ,    'properUnit': '',         'plotMin': 0,     'plotMax': 0, 'dbName': '', 'description': '' }, 
  'currentPrice'                  : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Price ($)',           'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'earningsGrowth'                : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 19,   'shortName': 'Earnings Growth',  'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'earningsGrowth_(pct)'          : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'calc',   'idxAnalysisPg': 19,   'shortName': 'Earnings Growth (%)',  'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'currentRatio'                  : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'CurrentRatio',    'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'returnOnAssets'                : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 13,   'shortName': 'ROA(%)',          'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'returnOnAssets_(pct)'          : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'calc',   'idxAnalysisPg': 13,   'shortName': 'ROA (%)',          'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'numberOfAnalystOpinions'       : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'no.Analyst',      'dType': 'int' ,    'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'targetMeanPrice'               : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Target Mean Price ($)','dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'debtToEquity'                  : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'DOE',             'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'returnOnEquity'                : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 14,   'shortName': 'ROE(%)',          'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'returnOnEquity_(pct)'          : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'calc',   'idxAnalysisPg': 14,   'shortName': 'ROE (%)',          'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'targetHighPrice'               : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Target High Price ($)','dType': 'int ',    'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'targetHigh_(pct)'              : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': None, 'shortName': 'Target High (%)','dType': 'int ',    'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalCash'                     : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Total Cash',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalCash_(M)'                 : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': None, 'shortName': 'Total Cash (M)',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalCash_(B)'                 : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': None, 'shortName': 'Total Cash (B)',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalDebt'                     : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Total Debt',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalDebt_(M)'                 : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': None, 'shortName': 'Total Debt (M)',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalDebt_(B)'                 : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': None, 'shortName': 'Total Debt (B)',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalRevenue'                  : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': 2,    'shortName': 'Total Revenue',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalRevenue_(M)'              : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': 2,    'shortName': 'Total Revenue (M)',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalRevenue_(B)'              : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': 2,    'shortName': 'Total Revenue (B)',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalCashPerShare'             : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Total Cash per Share',                'dType': 'float',   'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'financialCurrency'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Currency',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'revenuePerShare'               : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Revenue per Share',             'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'quickRatio'                    : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 7,    'shortName': 'QuickRatio (>1)', 'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'recommendationMean'            : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'MeanPrice',       'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'exchange'                      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Exchange',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'shortName'                     : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Name',            'dType': 'str' ,    'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'longName'                      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'exchangeTimezoneName'          : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'exchangeTimezoneShortName'     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'isEsgPopulated'                : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'gmtOffSetMilliseconds'         : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'quoteType'                     : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'symbol'                        : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Ticker',          'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'messageBoardId'                : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'market'                        : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'annualHoldingsTurnover'        : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'enterpriseToRevenue'           : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'enterpriseToRevenue', 'dType': 'float','properUnit': '',        'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'beta3Year'                     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Beta (3yrs)',     'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'enterpriseToEbitda'            : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  '52WeekChange'                  : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '52 Week Change',  'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1, 'plotMax': 1, 'dbName': '', 'description': '' }, 
  'morningStarRiskRating'         : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Morning Star Rating', 'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'forwardEps'                    : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'ForwardEPS',      'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'revenueQuarterlyGrowth'        : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Revenue Quarterly Growth', 'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'sharesOutstanding'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'nShare',          'dType': 'm/b' ,    'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fundInceptionDate'             : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Inception Date',  'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'annualReportExpenseRatio'      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'totalAssets'                   : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Total Assets',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'bookValue'                     : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Book Value',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'sharesShort'                   : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'm/b' ,    'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'sharesPercentSharesOut'        : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fundFamily'                    : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'lastFiscalYearEnd'             : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'heldPercentInstitutions'       : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'PctInstitution',  'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 1, 'dbName': '', 'description': '' }, 
  'netIncomeToCommon'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'trailingEps'                   : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'TrailingEPS',     'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'lastDividendValue'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'SandP52WeekChange'             : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'priceToBook'                   : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 11,   'shortName': 'PBV',             'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'heldPercentInsiders'           : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Insider (%)',      'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'nextFiscalYearEnd'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'datetime','properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'yield'                         : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'mostRecentQuarter'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'shortRatio'                    : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 9,    'shortName': 'Short Ratio',      'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 1, 'dbName': '', 'description': '' }, 
  'sharesShortPreviousMonthDate'  : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'floatShares'                   : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'm/b' ,    'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'beta'                          : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'Beta',            'dType': 'float' ,  'properUnit': '',         'plotMin': -0.3, 'plotMax': 5, 'dbName': '', 'description': '' }, 
  'enterpriseValue'               : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': 1,    'shortName': 'Enterprise Value',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'enterpriseValue_(B)'           : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': 1,    'shortName': 'Enterprise Value (B)',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'priceHint'                     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'threeYearAverageReturn'        : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'lastSplitDate'                 : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'datetime','properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'lastSplitFactor'               : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'legalType'                     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'lastDividendDate'              : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'datetime','properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'morningStarOverallRating'      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'earningsQuarterlyGrowth'       : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'EarningsQGrowth', 'dType': 'float' ,  'properUnit': 'pct',      'plotMin': -1, 'plotMax': 2, 'dbName': '', 'description': '' }, 
  'priceToSalesTrailing12Months'  : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'dateShortInterest'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'datetime','properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'pegRatio'                      : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 5,    'shortName': 'PEG (<1)',        'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 10, 'dbName': '', 'description': '' }, 
  'ytdReturn'                     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'forwardPE'                     : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 10,   'shortName': 'ForwardPE',       'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'lastCapGain'                   : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'shortPercentOfFloat'           : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'ShortPctFloat',   'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 3, 'dbName': '', 'description': '' }, 
  'sharesShortPriorMonth'         : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'impliedSharesOutstanding'      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'float' ,  'properUnit': 'm/b',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'category'                      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fiveYearAverageReturn'         : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'previousClose'                 : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'regularMarketOpen'             : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'twoHundredDayAverage'          : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '200 Days Avg ($)',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'trailingAnnualDividendYield'   : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'DIVYield',        'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0.3, 'dbName': '', 'description': '' }, 
  'payoutRatio'                   : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 8,    'shortName': 'Payout',          'dType': 'float' ,  'properUnit': 'pct',      'plotMin': 0, 'plotMax': 2, 'dbName': '', 'description': '' }, 
  'volume24Hr'                    : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'regularMarketDayHigh'          : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'navPrice'                      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'averageDailyVolume10Day'       : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'regularMarketPreviousClose'    : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fiftyDayAverage'               : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '50 Days Avg ($)',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'trailingAnnualDividendRate'    : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'open'                          : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'toCurrency'                    : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'averageVolume10days'           : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': 'float' ,  'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'expireDate'                    : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'algorithm'                     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'dividendRate'                  : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'DivRate',         'dType': '' ,       'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'exDividendDate'                : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': 'datetime', 'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'circulatingSupply'             : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'startDate'                     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'regularMarketDayLow'           : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'currency'                      : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'trailingPE'                    : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'TrailingPE',      'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'regularMarketVolume'           : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'lastMarket'                    : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'maxSupply'                     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'openInterest'                  : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'marketCap'                     : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': 0,    'shortName': 'MarketCap',       'dType': 'float' ,       'properUnit': 'm/b', 'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'marketCap_(B)'                 : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'calc',   'idxAnalysisPg': 0,    'shortName': 'MarketCap (B)',       'dType': 'float' ,       'properUnit': 'm/b', 'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'volumeAllCurrencies'           : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'strikePrice'                   : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'averageVolume'                 : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'dayLow'                        : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'ask'                           : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'askSize'                       : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'volume'                        : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fiftyTwoWeekHigh'              : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '52wks High ($)',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fiftyTwoWeekHigh_(pct)'        : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': None, 'shortName': '52wks High Chg (%)',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fromCurrency'                  : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fiveYearAvgDividendYield'      : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': '5Yr DivYield',    'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fiftyTwoWeekLow'               : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '52wks Low ($)',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'fiftyTwoWeekLow_(pct)'         : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '52wks Low Chg (%)',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'bid'                           : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'tradeable'                     : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'dividendYield'                 : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': 12,   'shortName': 'DivYield',        'dType': '' ,       'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'dividendYield_(pct)'           : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'calc',   'idxAnalysisPg': 12,   'shortName': 'Div Yield (%)',        'dType': '' ,       'properUnit': 'pct',      'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'bidSize'                       : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'dayHigh'                       : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'regularMarketPrice'            : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'preMarketPrice'                : {'keep': False, 'keepAnalysisPg': False, 'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'logo_url'                      : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':False, 'src': 'yf',   'idxAnalysisPg': None, 'shortName': '',                'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 0, 'dbName': '', 'description': '' }, 
  'trailingPegRatio'              : {'keep': True,  'keepAnalysisPg': False, 'keepComparison':True,  'src': 'yf',   'idxAnalysisPg': None, 'shortName': 'TrailingPEG',     'dType': '' ,       'properUnit': '',         'plotMin': 0, 'plotMax': 10, 'dbName': '', 'description': '' },
  # Calculation
  'ROEPBV'                        : {'keep': True,  'keepAnalysisPg': True,  'keepComparison':True,  'src': 'calc', 'idxAnalysisPg': 6,    'shortName': 'ROE/PBV (>5)',         'dType': 'float' ,  'properUnit': '', 'plotMin': 0, 'plotMax': 10, 'dbName': '', 'description': '' },
}

dfDataInfoParams = pd.DataFrame(dictDataInfoParams)

dictShortName = {}
for item in dfDataInfoParams:
  dictShortName[item] = dfDataInfoParams[item]["shortName"]

from st_aggrid.shared import JsCode

cellstyle_jscode_pegRatio = JsCode(
    """
function(params) {
    if (params.value < 1 & params.value > 0) {
        return {
            'color': 'white',
            'backgroundColor': '#508484'
        }
    } else {
        return {
            'color': 'black',
            'backgroundColor': 'white'
        }
    }
};
"""
)
cellstyle_jscode_ROEPBV = JsCode(
    """
function(params) {
    if (params.value > 5) {
        return {
            'color': 'white',
            'backgroundColor': '#508484'
        }
    } else {
        return {
            'color': 'black',
            'backgroundColor': 'white'
        }
    }
};
"""
)
cellstyle_jscode_quickRatio = JsCode(
    """
function(params) {
    if (params.value > 1) {
        return {
            'color': 'white',
            'backgroundColor': '#508484'
        }
    } else {
        return {
            'color': 'black',
            'backgroundColor': 'white'
        }
    }
};
"""
)
cellstyle_jscode_UpDown = JsCode(
    """
function(params) {
    if (params.value > 30) {
        return {
            'color': 'white',
            'backgroundColor': '#508484'
        }
    } else {
        return {
            'color': 'black',
            'backgroundColor': 'white'
        }
    }
};
"""
)

# =============================================================================================================
# FUNCTIONS\
# 
def convertyfinfo2df(datainfo, dictDataInfoParams, keyKeep = 'keep'):
  
  dictDataInfo = {}

  # Organizing data
  for key in dictDataInfoParams:
    if np.logical_and(dictDataInfoParams[key][keyKeep] == True ,dictDataInfoParams[key]['src'] == 'yf'):

      # Check the type of data
      try:
        tempData = datainfo[key]

        if type(datainfo[key]) != str:
        # If it is the number, check the type of number
          if dictDataInfoParams[key]['dType'] == 'int':
            dictDataInfo[key] = int(tempData)
          elif dictDataInfoParams[key]['dType'] == 'datetime':
            dictDataInfo[key] = datetime.fromtimestamp(tempData).strftime('%Y%m%d')
          else:
            dictDataInfo[key] = np.round(tempData, decimals = 2)
        else:
          dictDataInfo[key] = tempData
      except:
        dictDataInfo[key] = np.nan

      # Extra calculation based on this 
      if dictDataInfoParams[key]['properUnit'] == 'm/b':
        try:
          dictDataInfo[key + '_(B)'] = dictDataInfo[key]/1000000000
          dictDataInfo[key + '_(M)'] = dictDataInfo[key]/1000000
        except:
          dictDataInfo[key + '_(B)'] = np.nan
          dictDataInfo[key + '_(M)'] = np.nan
      if dictDataInfoParams[key]['properUnit'] == 'pct':
        try:
          dictDataInfo[key + '_(pct)'] = dictDataInfo[key]*100
          dictDataInfo[key + '_(pct_str)'] = '%.0f' % (dictDataInfo[key]*100) + '%' 
        except:
          dictDataInfo[key + '_(pct)'] =  np.nan
          dictDataInfo[key + '_(pct_str)'] = np.nan

  # Add all extra calculation here:
  try: 
    dictDataInfo["ROEPBV"] = np.round(datainfo["returnOnEquity"]*100/datainfo["priceToBook"])
  except:
    dictDataInfo["ROEPBV"] = np.nan
  try:
    dictDataInfo['dailyChange']       = (dictDataInfo['currentPrice'] - dictDataInfo['previousClose'])/dictDataInfo['previousClose']
    dictDataInfo['200DayAvgChange']   = (dictDataInfo['currentPrice'] - dictDataInfo['twoHundredDayAverage'])/dictDataInfo['twoHundredDayAverage']
    dictDataInfo['50DayAvgChange']    = (dictDataInfo['currentPrice'] - dictDataInfo['fiftyDayAverage'])/dictDataInfo['fiftyDayAverage']
    dictDataInfo['10DayVolumeChange'] = (dictDataInfo['averageVolume'] - dictDataInfo['averageDailyVolume10Day'])/dictDataInfo['averageDailyVolume10Day']
    dictDataInfo['dailyChange_(pct)']       = (dictDataInfo['currentPrice'] - dictDataInfo['previousClose'])/dictDataInfo['previousClose']*100
    dictDataInfo['200DayAvgChange_(pct)']   = (dictDataInfo['currentPrice'] - dictDataInfo['twoHundredDayAverage'])/dictDataInfo['twoHundredDayAverage']*100
    dictDataInfo['50DayAvgChange_(pct)']    = (dictDataInfo['currentPrice'] - dictDataInfo['fiftyDayAverage'])/dictDataInfo['fiftyDayAverage']*100
    dictDataInfo['10DayVolumeChange_(pct)'] = (dictDataInfo['averageVolume'] - dictDataInfo['averageDailyVolume10Day'])/dictDataInfo['averageDailyVolume10Day']*100 
    dictDataInfo['targetLow_(pct)']   = (dictDataInfo['targetLowPrice'] - dictDataInfo['currentPrice'])/dictDataInfo['currentPrice']*100
    dictDataInfo['targetMedian_(pct)']= (dictDataInfo['targetMedianPrice'] - dictDataInfo['currentPrice'])/dictDataInfo['currentPrice']*100
    dictDataInfo['targetHigh_(pct)']  = (dictDataInfo['targetHighPrice'] - dictDataInfo['currentPrice'])/dictDataInfo['currentPrice']*100
    dictDataInfo['fiftyTwoWeekHigh_(pct)']  = (dictDataInfo['fiftyTwoWeekHigh'] - dictDataInfo['currentPrice'])/dictDataInfo['currentPrice']*100
    dictDataInfo['fiftyTwoWeekLow_(pct)']  = (dictDataInfo['fiftyTwoWeekLow'] - dictDataInfo['currentPrice'])/dictDataInfo['currentPrice']*100
  except:
    dictDataInfo['dailyChange']             = np.nan
    dictDataInfo['200DayAvgChange']         = np.nan
    dictDataInfo['50DayAvgChange']          = np.nan
    dictDataInfo['10DayVolumeChange']       = np.nan
    dictDataInfo['dailyChange_(pct)']       = np.nan
    dictDataInfo['200DayAvgChange_(pct)']   = np.nan
    dictDataInfo['50DayAvgChange_(pct)']    = np.nan
    dictDataInfo['10DayVolumeChange_(pct)'] = np.nan
    dictDataInfo['targetLow_(pct)']         = np.nan
    dictDataInfo['targetMedian_(pct)']      = np.nan
    dictDataInfo['targetHigh_(pct)']        = np.nan




  dfDataInfo = pd.DataFrame(dictDataInfo, index=[0])
  return dfDataInfo

def parseTicker(tempTicker, parseSymbol = "::"):
  iParse      = tempTicker.find(parseSymbol) 
  if iParse > 1:
    nameTicker  = tempTicker[:int(iParse)]
  else:
    nameTicker = tempTicker
  return nameTicker

def calcRSI(data, window=14, adjust=False):
    delta = data['Close'].diff(1).dropna()
    loss = delta.copy()
    gains = delta.copy()

    gains[gains < 0] = 0
    loss[loss > 0] = 0

    gain_ewm = gains.ewm(com=window - 1, adjust=adjust).mean()
    loss_ewm = abs(loss.ewm(com=window - 1, adjust=adjust).mean())

    RS = gain_ewm / loss_ewm
    RSI = 100 - 100 / (1 + RS)

    return RSI

def calcGrowth(dfFinancial):

  dfFinancial = dfFinancial.sort_index(ascending= True)

  for key in dfFinancial:
    try:
      dfFinancial[key + '_Growth(pct)'] = dfFinancial[key].diff()/dfFinancial[key].shift(periods =1) * 100
      dfFinancial[key + '_Growth(pct)'] = dfFinancial[key + '_Growth(pct)'].astype(float).round(2)
    except:
      dfFinancial[key + '_Growth(pct)'] = np.nan
    
  return dfFinancial

def cleanList(listData):
  listData        = list(filter(None, listData))
  listData        = set(listData)
  listData_clean  = [x for x in listData if str(x) != 'nan']
  return listData_clean
