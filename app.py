# =============================================================================================================
# Trade Screener
# =============================================================================================================
# NOTE

# =============================================================================================================
# LOAD TOOLBOX
from curses import keyname
import time
import os
from io import BytesIO
import copy

time_start      = time.time()ß
timetrack       = {}

# Streamlit
import streamlit as st
from   streamlit import session_state as ss
from   streamlit_option_menu import option_menu
import streamlit.components.v1 as html

# General
import numpy as np
import pandas as pd
pd.set_option('display.precision', 2)
import yfinance as yf
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from   plotly.subplots import make_subplots
from scipy.stats import pearsonr, norm
from math import log, sqrt, exp, pi
from plotly_calplot import calplot
from   flask import request
from   sstoolbox import *

# Time
from   datetime import datetime, timedelta, date
import calendar
import datetime as dt
from dateutil.relativedelta import *
from time import strptime
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, USLaborDay, USThanksgivingDay

# Sheet 
import pygsheets
import pickle


# =============================================================================================================
# PAGE SETUP
st.set_page_config(
    page_title            = 'tradescreener',
    page_icon             = ":chart_with_upwards_trend:",
    layout                = 'wide',
    initial_sidebar_state = 'auto',
    menu_items            = {}
    )
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.write(
  """
  <style>
  [data-testid="stMetricDelta"] svg {
      display: none;
  }
  </style>
  """,
  unsafe_allow_html=True,
)
# Hide made by streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# =============================================================================================================
# SESSION_STATE (time taken 3s here)

timetrack['start session state'] = np.round(time.time() - time_start)

# gc = pygsheets.authorize(service_account_file= 'client_secret.json')

if len(ss) == 0:

    timetrack['load python toolbox'] = np.round(time.time() - time_start)
    # Current Date
    ss.currentDate                = datetime.now().strftime('%Y%m%d') 
    ss.currentDay                 = datetime.now().strftime('%d') 
    ss.currentMonth               = datetime.now().strftime('%m') 
    ss.currentYear                = datetime.now().strftime('%Y') 
    ss.previousDate               = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

    # General Initialization
    ss.ip_address           = None
    ss.nameTicker           = 'AAPL'
    ss.listTicker           = ["MSFT", "AAPL", "NVDA", "TSLA", "GOOGL", "META", "AMZN"]

  # # Load Data
  # ss.data = yf.Ticker(ss.nameTicker)
  # ss.dfDataAnalysis = convertyfinfo2df(ss.data.info, dictDataInfoParams, keyKeep = 'keepAnalysisPg')

  # Tracker
    ss.validTicker          = False
    ss.boolLoadComparison   = False

    # For manipulate table for comparison 
    ss.dictKeyComparison = { 
                    "symbol"              : "Ticker",
                    "shortName"           : "Name",
                    "recommendationKey"   : "Recommend",
                    "Upside(%)"           : "Upside(%)",
                    "profitMargins_(pct)" : "Profit Margin(%)",
                    "earningsGrowth_(pct)": "Earnings Growth(%)",
                    "pegRatio"            : "PEG",
                    "ROEPBV"              : "ROE/PBV",
                    "quickRatio"          : "QuickRatio",
                    }

    ss.dfOptionCall_all         = pd.DataFrame()
    ss.dfOptionPut_all          = pd.DataFrame()
    ss.boolAggregateColumn      = False
    ss.dateOption               = None

    ss.boolFirstLoad            = True
    ss.data                     = None 
    ss.dfDataAnalysis           = None

  # TODO Occasionally update this list - download the updates on S&P500 List
    ss.dictSP500 = {0: {'Symbol': 'MMM', 'Security': '3M', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Conglomerates','Date added': '1957-03-04','Founded': '1902'},
 1: {'Symbol': 'AOS', 'Security': 'A. O. Smith', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Building Products','Date added': '2017-07-26','Founded': '1916'},
 2: {'Symbol': 'ABT', 'Security': 'Abbott', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '1957-03-04','Founded': '1888'},
 3: {'Symbol': 'ABBV', 'Security': 'AbbVie', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Biotechnology','Date added': '2012-12-31','Founded': '2013 (1888)'},
 4: {'Symbol': 'ACN', 'Security': 'Accenture', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'IT Consulting & Other Services','Date added': '2011-07-06','Founded': '1989'},
 5: {'Symbol': 'ADBE', 'Security': 'Adobe Inc.', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '1997-05-05','Founded': '1982'},
 6: {'Symbol': 'AMD', 'Security': 'Advanced Micro Devices', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2017-03-20','Founded': '1969'},
 7: {'Symbol': 'AES', 'Security': 'AES Corporation', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Independent Power Producers & Energy Traders','Date added': '1998-10-02','Founded': '1981'},
 8: {'Symbol': 'AFL', 'Security': 'Aflac', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Life & Health Insurance','Date added': '1999-05-28','Founded': '1955'},
 9: {'Symbol': 'A', 'Security': 'Agilent Technologies', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '2000-06-05','Founded': '1999'},
 10: {'Symbol': 'APD', 'Security': 'Air Products and Chemicals', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Industrial Gases','Date added': '1985-04-30','Founded': '1940'},
 11: {'Symbol': 'ABNB', 'Security': 'Airbnb', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Hotels, Resorts & Cruise Lines','Date added': '2023-09-18','Founded': '2008'},
 12: {'Symbol': 'AKAM', 'Security': 'Akamai', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Internet Services & Infrastructure','Date added': '2007-07-12','Founded': '1998'},
 13: {'Symbol': 'ALB', 'Security': 'Albemarle Corporation', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '2016-07-01','Founded': '1994'},
 14: {'Symbol': 'ARE', 'Security': 'Alexandria Real Estate Equities', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Office REITs','Date added': '2017-03-20','Founded': '1994'},
 15: {'Symbol': 'ALGN', 'Security': 'Align Technology', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Supplies','Date added': '2017-06-19','Founded': '1997'},
 16: {'Symbol': 'ALLE', 'Security': 'Allegion', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Building Products','Date added': '2013-12-02','Founded': '1908'},
 17: {'Symbol': 'LNT', 'Security': 'Alliant Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '2016-07-01','Founded': '1917'},
 18: {'Symbol': 'ALL', 'Security': 'Allstate', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Property & Casualty Insurance','Date added': '1995-07-13','Founded': '1931'},
 19: {'Symbol': 'GOOGL', 'Security': 'Alphabet Inc. (Class A)', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Interactive Media & Services','Date added': '2014-04-03','Founded': '1998'},
 20: {'Symbol': 'GOOG', 'Security': 'Alphabet Inc. (Class C)', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Interactive Media & Services','Date added': '2006-04-03','Founded': '1998'},
 21: {'Symbol': 'MO', 'Security': 'Altria', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Tobacco','Date added': '1957-03-04','Founded': '1985'},
 22: {'Symbol': 'AMZN', 'Security': 'Amazon', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Broadline Retail','Date added': '2005-11-18','Founded': '1994'},
 23: {'Symbol': 'AMCR', 'Security': 'Amcor', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Paper & Plastic Packaging Products & Materials','Date added': '2019-06-07','Founded': '2019 (1860)'},
 24: {'Symbol': 'AEE', 'Security': 'Ameren', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '1991-09-19','Founded': '1902'},
 25: {'Symbol': 'AAL', 'Security': 'American Airlines Group', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Passenger Airlines','Date added': '2015-03-23','Founded': '1934'},
 26: {'Symbol': 'AEP', 'Security': 'American Electric Power', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '1957-03-04','Founded': '1906'},
 27: {'Symbol': 'AXP', 'Security': 'American Express', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Consumer Finance','Date added': '1976-06-30','Founded': '1850'},
 28: {'Symbol': 'AIG', 'Security': 'American International Group', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Multi-line Insurance','Date added': '1980-03-31','Founded': '1919'},
 29: {'Symbol': 'AMT', 'Security': 'American Tower', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Telecom Tower REITs','Date added': '2007-11-19','Founded': '1995'},
 30: {'Symbol': 'AWK', 'Security': 'American Water Works', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Water Utilities','Date added': '2016-03-04','Founded': '1886'},
 31: {'Symbol': 'AMP', 'Security': 'Ameriprise Financial', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '2005-10-03','Founded': '1894'},
 32: {'Symbol': 'AME', 'Security': 'Ametek', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Electrical Components & Equipment','Date added': '2013-09-23','Founded': '1930'},
 33: {'Symbol': 'AMGN', 'Security': 'Amgen', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Biotechnology','Date added': '1992-01-02','Founded': '1980'},
 34: {'Symbol': 'APH', 'Security': 'Amphenol', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Components','Date added': '2008-09-30','Founded': '1932'},
 35: {'Symbol': 'ADI', 'Security': 'Analog Devices', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '1999-10-12','Founded': '1965'},
 36: {'Symbol': 'ANSS', 'Security': 'Ansys', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '2017-06-19','Founded': '1969'},
 37: {'Symbol': 'AON', 'Security': 'Aon', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Insurance Brokers','Date added': '1996-04-23','Founded': '1982 (1919)'},
 38: {'Symbol': 'APA', 'Security': 'APA Corporation', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '1997-07-28','Founded': '1954'},
 39: {'Symbol': 'AAPL', 'Security': 'Apple Inc.', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Technology Hardware, Storage & Peripherals','Date added': '1982-11-30','Founded': '1977'},
 40: {'Symbol': 'AMAT', 'Security': 'Applied Materials', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductor Materials & Equipment','Date added': '1995-03-16','Founded': '1967'},
 41: {'Symbol': 'APTV', 'Security': 'Aptiv', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Automotive Parts & Equipment','Date added': '2012-12-24','Founded': '1994'},
 42: {'Symbol': 'ACGL', 'Security': 'Arch Capital Group', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Property & Casualty Insurance','Date added': '2022-11-01','Founded': '1995'},
 43: {'Symbol': 'ADM', 'Security': 'Archer-Daniels-Midland', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Agricultural Products & Services','Date added': '1957-03-04','Founded': '1902'},
 44: {'Symbol': 'ANET', 'Security': 'Arista Networks', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Communications Equipment','Date added': '2018-08-28','Founded': '2004'},
 45: {'Symbol': 'AJG', 'Security': 'Arthur J. Gallagher & Co.', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Insurance Brokers','Date added': '2016-05-31','Founded': '1927'},
 46: {'Symbol': 'AIZ', 'Security': 'Assurant', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Multi-line Insurance','Date added': '2007-04-10','Founded': '1892'},
 47: {'Symbol': 'T', 'Security': 'AT&T', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Integrated Telecommunication Services','Date added': '1983-11-30','Founded': '1983 (1885)'},
 48: {'Symbol': 'ATO', 'Security': 'Atmos Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Gas Utilities','Date added': '2019-02-15','Founded': '1906'},
 49: {'Symbol': 'ADSK', 'Security': 'Autodesk', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '1989-12-01','Founded': '1982'},
 50: {'Symbol': 'ADP', 'Security': 'Automatic Data Processing', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Human Resource & Employment Services','Date added': '1981-03-31','Founded': '1949'},
 51: {'Symbol': 'AZO', 'Security': 'AutoZone', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Automotive Retail','Date added': '1997-01-02','Founded': '1979'},
 52: {'Symbol': 'AVB', 'Security': 'AvalonBay Communities', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Multi-Family Residential REITs','Date added': '2007-01-10','Founded': '1978'},
 53: {'Symbol': 'AVY', 'Security': 'Avery Dennison', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Paper & Plastic Packaging Products & Materials','Date added': '1987-12-31','Founded': '1990'},
 54: {'Symbol': 'AXON', 'Security': 'Axon Enterprise', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '2023-05-04','Founded': '1993'},
 55: {'Symbol': 'BKR', 'Security': 'Baker Hughes', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Equipment & Services','Date added': '2017-07-07','Founded': '2017'},
 56: {'Symbol': 'BALL', 'Security': 'Ball Corporation', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Metal, Glass & Plastic Containers','Date added': '1984-10-31','Founded': '1880'},
 57: {'Symbol': 'BAC', 'Security': 'Bank of America', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Diversified Banks','Date added': '1976-06-30','Founded': '1998 (1923 / 1874)'},
 58: {'Symbol': 'BK', 'Security': 'Bank of New York Mellon', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '1995-03-31','Founded': '1784'},
 59: {'Symbol': 'BBWI', 'Security': 'Bath & Body Works, Inc.', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Other Specialty Retail','Date added': '1983-09-30','Founded': '1963'},
 60: {'Symbol': 'BAX', 'Security': 'Baxter International', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '1972-09-30','Founded': '1931'},
 61: {'Symbol': 'BDX', 'Security': 'Becton Dickinson', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '1972-09-30','Founded': '1897'},
 62: {'Symbol': 'BRK.B', 'Security': 'Berkshire Hathaway', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Multi-Sector Holdings','Date added': '2010-02-16','Founded': '1839'},
 63: {'Symbol': 'BBY', 'Security': 'Best Buy', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Computer & Electronics Retail','Date added': '1999-06-29','Founded': '1966'},
 64: {'Symbol': 'BIO', 'Security': 'Bio-Rad', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '2020-06-22','Founded': '1952'},
 65: {'Symbol': 'TECH', 'Security': 'Bio-Techne', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '2021-08-30','Founded': '1976'},
 66: {'Symbol': 'BIIB', 'Security': 'Biogen', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Biotechnology','Date added': '2003-11-13','Founded': '1978'},
 67: {'Symbol': 'BLK', 'Security': 'BlackRock', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '2011-04-04','Founded': '1988'},
 68: {'Symbol': 'BX', 'Security': 'Blackstone', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '2023-09-18','Founded': '1985'},
 69: {'Symbol': 'BA', 'Security': 'Boeing', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '1957-03-04','Founded': '1916'},
 70: {'Symbol': 'BKNG', 'Security': 'Booking Holdings', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Hotels, Resorts & Cruise Lines','Date added': '2009-11-06','Founded': '1996'},
 71: {'Symbol': 'BWA', 'Security': 'BorgWarner', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Automotive Parts & Equipment','Date added': '2011-12-19','Founded': '1880'},
 72: {'Symbol': 'BXP', 'Security': 'Boston Properties', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Office REITs','Date added': '2006-04-03','Founded': '1970'},
 73: {'Symbol': 'BSX', 'Security': 'Boston Scientific', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '1995-02-24','Founded': '1979'},
 74: {'Symbol': 'BMY', 'Security': 'Bristol Myers Squibb', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Pharmaceuticals','Date added': '1957-03-04','Founded': '1989 (1887)'},
 75: {'Symbol': 'AVGO', 'Security': 'Broadcom Inc.', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2014-05-08','Founded': '1961'},
 76: {'Symbol': 'BR', 'Security': 'Broadridge Financial Solutions', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Data Processing & Outsourced Services','Date added': '2018-06-18','Founded': '1962'},
 77: {'Symbol': 'BRO', 'Security': 'Brown & Brown', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Insurance Brokers','Date added': '2021-09-20','Founded': '1939'},
 78: {'Symbol': 'BF.B', 'Security': 'Brown–Forman', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Distillers & Vintners','Date added': '1982-10-31','Founded': '1870'},
 79: {'Symbol': 'BLDR', 'Security': 'Builders FirstSource', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Building Products','Date added': '2023-12-18','Founded': '1998'},
 80: {'Symbol': 'BG', 'Security': 'Bunge Global SA', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Agricultural Products & Services','Date added': '2023-03-15','Founded': '1818'},
 81: {'Symbol': 'CDNS', 'Security': 'Cadence Design Systems', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '2017-09-18','Founded': '1988'},
 82: {'Symbol': 'CZR', 'Security': 'Caesars Entertainment', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Casinos & Gaming','Date added': '2021-03-22','Founded': '1973'},
 83: {'Symbol': 'CPT', 'Security': 'Camden Property Trust', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Multi-Family Residential REITs','Date added': '2022-04-04','Founded': '1981'},
 84: {'Symbol': 'CPB', 'Security': 'Campbell Soup Company', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '1957-03-04','Founded': '1869'},
 85: {'Symbol': 'COF', 'Security': 'Capital One', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Consumer Finance','Date added': '1998-07-01','Founded': '1994'},
 86: {'Symbol': 'CAH', 'Security': 'Cardinal Health', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Distributors','Date added': '1997-05-27','Founded': '1971'},
 87: {'Symbol': 'KMX', 'Security': 'CarMax', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Automotive Retail','Date added': '2010-06-28','Founded': '1993'},
 88: {'Symbol': 'CCL', 'Security': 'Carnival', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Hotels, Resorts & Cruise Lines','Date added': '1998-12-22','Founded': '1972'},
 89: {'Symbol': 'CARR', 'Security': 'Carrier Global', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Building Products','Date added': '2020-04-03','Founded': '2020 (1915, United Technologies spinoff)'},
 90: {'Symbol': 'CTLT', 'Security': 'Catalent', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Pharmaceuticals','Date added': '2020-09-21','Founded': '2007'},
 91: {'Symbol': 'CAT', 'Security': 'Caterpillar Inc.', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Construction Machinery & Heavy Transportation Equipment','Date added': '1957-03-04','Founded': '1925'},
 92: {'Symbol': 'CBOE', 'Security': 'Cboe Global Markets', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '2017-03-01','Founded': '1973'},
 93: {'Symbol': 'CBRE', 'Security': 'CBRE Group', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Real Estate Services','Date added': '2006-11-10','Founded': '1906'},
 94: {'Symbol': 'CDW', 'Security': 'CDW', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Technology Distributors','Date added': '2019-09-23','Founded': '1984'},
 95: {'Symbol': 'CE', 'Security': 'Celanese', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '2018-12-24','Founded': '1918'},
 96: {'Symbol': 'COR', 'Security': 'Cencora', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Distributors','Date added': '2001-08-30','Founded': '1985'},
 97: {'Symbol': 'CNC', 'Security': 'Centene Corporation', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Managed Health Care','Date added': '2016-03-30','Founded': '1984'},
 98: {'Symbol': 'CNP', 'Security': 'CenterPoint Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '1985-07-31','Founded': '1882'},
 99: {'Symbol': 'CF', 'Security': 'CF Industries', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Fertilizers & Agricultural Chemicals','Date added': '2008-08-27','Founded': '1946'},
 100: {'Symbol': 'CHRW', 'Security': 'CH Robinson', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Air Freight & Logistics','Date added': '2007-03-02','Founded': '1905'},
 101: {'Symbol': 'CRL', 'Security': 'Charles River Laboratories', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '2021-05-14','Founded': '1947'},
 102: {'Symbol': 'SCHW', 'Security': 'Charles Schwab Corporation', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Investment Banking & Brokerage','Date added': '1997-06-02','Founded': '1971'},
 103: {'Symbol': 'CHTR', 'Security': 'Charter Communications', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Cable & Satellite','Date added': '2016-09-08','Founded': '1993'},
 104: {'Symbol': 'CVX', 'Security': 'Chevron Corporation', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Integrated Oil & Gas','Date added': '1957-03-04','Founded': '1879'},
 105: {'Symbol': 'CMG', 'Security': 'Chipotle Mexican Grill', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Restaurants','Date added': '2011-04-28','Founded': '1993'},
 106: {'Symbol': 'CB', 'Security': 'Chubb Limited', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Property & Casualty Insurance','Date added': '2010-07-15','Founded': '1985'},
 107: {'Symbol': 'CHD', 'Security': 'Church & Dwight', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Household Products','Date added': '2015-12-29','Founded': '1847'},
 108: {'Symbol': 'CI', 'Security': 'Cigna', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Services','Date added': '1976-06-30','Founded': '1982'},
 109: {'Symbol': 'CINF', 'Security': 'Cincinnati Financial', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Property & Casualty Insurance','Date added': '1997-12-18','Founded': '1950'},
 110: {'Symbol': 'CTAS', 'Security': 'Cintas', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Diversified Support Services','Date added': '2001-03-01','Founded': '1929'},
 111: {'Symbol': 'CSCO', 'Security': 'Cisco', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Communications Equipment','Date added': '1993-12-01','Founded': '1984'},
 112: {'Symbol': 'C', 'Security': 'Citigroup', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Diversified Banks','Date added': '1988-05-31','Founded': '1998'},
 113: {'Symbol': 'CFG', 'Security': 'Citizens Financial Group', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Regional Banks','Date added': '2016-01-29','Founded': '1828'},
 114: {'Symbol': 'CLX', 'Security': 'Clorox', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Household Products','Date added': '1969-03-31','Founded': '1913'},
 115: {'Symbol': 'CME', 'Security': 'CME Group', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '2006-08-11','Founded': '1848'},
 116: {'Symbol': 'CMS', 'Security': 'CMS Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '1957-03-04','Founded': '1886'},
 117: {'Symbol': 'KO', 'Security': 'Coca-Cola Company (The)', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Soft Drinks & Non-alcoholic Beverages','Date added': '1957-03-04','Founded': '1886'},
 118: {'Symbol': 'CTSH', 'Security': 'Cognizant', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'IT Consulting & Other Services','Date added': '2006-11-17','Founded': '1994'},
 119: {'Symbol': 'CL', 'Security': 'Colgate-Palmolive', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Household Products','Date added': '1957-03-04','Founded': '1806'},
 120: {'Symbol': 'CMCSA', 'Security': 'Comcast', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Cable & Satellite','Date added': '2002-11-19','Founded': '1963'},
 121: {'Symbol': 'CAG', 'Security': 'Conagra Brands', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '1983-08-31','Founded': '1919'},
 122: {'Symbol': 'COP', 'Security': 'ConocoPhillips', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '1957-03-04','Founded': '2002'},
 123: {'Symbol': 'ED', 'Security': 'Consolidated Edison', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '1957-03-04','Founded': '1823'},
 124: {'Symbol': 'STZ', 'Security': 'Constellation Brands', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Distillers & Vintners','Date added': '2005-07-01','Founded': '1945'},
 125: {'Symbol': 'CEG', 'Security': 'Constellation Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '2022-02-02','Founded': '1999'},
 126: {'Symbol': 'COO', 'Security': 'CooperCompanies', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Supplies','Date added': '2016-09-23','Founded': '1958'},
 127: {'Symbol': 'CPRT', 'Security': 'Copart', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Diversified Support Services','Date added': '2018-07-02','Founded': '1982'},
 128: {'Symbol': 'GLW', 'Security': 'Corning Inc.', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Components','Date added': '1995-02-27','Founded': '1851'},
 129: {'Symbol': 'CPAY', 'Security': 'Corpay', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Transaction & Payment Processing Services','Date added': '2018-06-20','Founded': '2000'},
 130: {'Symbol': 'CTVA', 'Security': 'Corteva', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Fertilizers & Agricultural Chemicals','Date added': '2019-06-03','Founded': '2019'},
 131: {'Symbol': 'CSGP', 'Security': 'CoStar Group', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Real Estate Services','Date added': '2022-09-19','Founded': '1987'},
 132: {'Symbol': 'COST', 'Security': 'Costco', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Consumer Staples Merchandise Retail','Date added': '1993-10-01','Founded': '1976'},
 133: {'Symbol': 'CTRA', 'Security': 'Coterra', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '2008-06-23','Founded': '2021 (1989)'},
 134: {'Symbol': 'CRWD', 'Security': 'CrowdStrike', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Systems Software','Date added': '2024-06-24','Founded': '2011'},
 135: {'Symbol': 'CCI', 'Security': 'Crown Castle', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Telecom Tower REITs','Date added': '2012-03-14','Founded': '1994'},
 136: {'Symbol': 'CSX', 'Security': 'CSX', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Rail Transportation','Date added': '1957-03-04','Founded': '1980'},
 137: {'Symbol': 'CMI', 'Security': 'Cummins', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Construction Machinery & Heavy Transportation Equipment','Date added': '1965-03-31','Founded': '1919'},
 138: {'Symbol': 'CVS', 'Security': 'CVS Health', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Services','Date added': '1957-03-04','Founded': '1996'},
 139: {'Symbol': 'DHR', 'Security': 'Danaher Corporation', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '1998-11-18','Founded': '1969'},
 140: {'Symbol': 'DRI', 'Security': 'Darden Restaurants', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Restaurants','Date added': '1995-05-31','Founded': '1938'},
 141: {'Symbol': 'DVA', 'Security': 'DaVita Inc.', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Services','Date added': '2008-07-31','Founded': '1979'},
 142: {'Symbol': 'DAY', 'Security': 'Dayforce', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Human Resource & Employment Services','Date added': '2021-09-20','Founded': '1992'},
 143: {'Symbol': 'DECK', 'Security': 'Deckers Brands', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Footwear','Date added': '2024-03-18','Founded': '1973'},
 144: {'Symbol': 'DE', 'Security': 'John Deere', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Agricultural & Farm Machinery','Date added': '1957-03-04','Founded': '1837'},
 145: {'Symbol': 'DAL', 'Security': 'Delta Air Lines', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Passenger Airlines','Date added': '2013-09-11','Founded': '1929'},
 146: {'Symbol': 'DVN', 'Security': 'Devon Energy', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '2000-08-30','Founded': '1971'},
 147: {'Symbol': 'DXCM', 'Security': 'Dexcom', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2020-05-12','Founded': '1999'},
 148: {'Symbol': 'FANG', 'Security': 'Diamondback Energy', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '2018-12-03','Founded': '2007'},
 149: {'Symbol': 'DLR', 'Security': 'Digital Realty', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Data Center REITs','Date added': '2016-05-18','Founded': '2004'},
 150: {'Symbol': 'DFS', 'Security': 'Discover Financial', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Consumer Finance','Date added': '2007-07-02','Founded': '1985'},
 151: {'Symbol': 'DG', 'Security': 'Dollar General', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Consumer Staples Merchandise Retail','Date added': '2012-12-03','Founded': '1939'},
 152: {'Symbol': 'DLTR', 'Security': 'Dollar Tree', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Consumer Staples Merchandise Retail','Date added': '2011-12-19','Founded': '1986'},
 153: {'Symbol': 'D', 'Security': 'Dominion Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '2016-11-30','Founded': '1983'},
 154: {'Symbol': 'DPZ', 'Security': "Domino's", 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Restaurants','Date added': '2020-05-12','Founded': '1960'},
 155: {'Symbol': 'DOV', 'Security': 'Dover Corporation', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '1985-10-31','Founded': '1955'},
 156: {'Symbol': 'DOW', 'Security': 'Dow Inc.', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Commodity Chemicals','Date added': '2019-04-01','Founded': '2019 (1897)'},
 157: {'Symbol': 'DHI', 'Security': 'DR Horton', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Homebuilding','Date added': '2005-06-22','Founded': '1978'},
 158: {'Symbol': 'DTE', 'Security': 'DTE Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '1957-03-04','Founded': '1995'},
 159: {'Symbol': 'DUK', 'Security': 'Duke Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '1976-06-30','Founded': '1904'},
 160: {'Symbol': 'DD', 'Security': 'DuPont', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '2019-04-02','Founded': '2017 (1802)'},
 161: {'Symbol': 'EMN', 'Security': 'Eastman Chemical Company', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '1994-01-01','Founded': '1920'},
 162: {'Symbol': 'ETN', 'Security': 'Eaton Corporation', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Electrical Components & Equipment','Date added': '1957-03-04','Founded': '1911'},
 163: {'Symbol': 'EBAY', 'Security': 'eBay', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Broadline Retail','Date added': '2002-07-22','Founded': '1995'},
 164: {'Symbol': 'ECL', 'Security': 'Ecolab', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '1989-01-31','Founded': '1923'},
 165: {'Symbol': 'EIX', 'Security': 'Edison International', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '1957-03-04','Founded': '1886'},
 166: {'Symbol': 'EW', 'Security': 'Edwards Lifesciences', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2011-04-01','Founded': '1958'},
 167: {'Symbol': 'EA', 'Security': 'Electronic Arts', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Interactive Home Entertainment','Date added': '2002-07-22','Founded': '1982'},
 168: {'Symbol': 'ELV', 'Security': 'Elevance Health', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Managed Health Care','Date added': '2002-07-25','Founded': '2014 (1946)'},
 169: {'Symbol': 'LLY', 'Security': 'Eli Lilly and Company', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Pharmaceuticals','Date added': '1970-12-31','Founded': '1876'},
 170: {'Symbol': 'EMR', 'Security': 'Emerson Electric', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Electrical Components & Equipment','Date added': '1965-03-31','Founded': '1890'},
 171: {'Symbol': 'ENPH', 'Security': 'Enphase', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductor Materials & Equipment','Date added': '2021-01-07','Founded': '2006'},
 172: {'Symbol': 'ETR', 'Security': 'Entergy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '1957-03-04','Founded': '1913'},
 173: {'Symbol': 'EOG', 'Security': 'EOG Resources', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '2000-11-02','Founded': '1999'},
 174: {'Symbol': 'EPAM', 'Security': 'EPAM Systems', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'IT Consulting & Other Services','Date added': '2021-12-14','Founded': '1993'},
 175: {'Symbol': 'EQT', 'Security': 'EQT Corporation', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '2022-10-03','Founded': '1888'},
 176: {'Symbol': 'EFX', 'Security': 'Equifax', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Research & Consulting Services','Date added': '1997-06-19','Founded': '1899'},
 177: {'Symbol': 'EQIX', 'Security': 'Equinix', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Data Center REITs','Date added': '2015-03-20','Founded': '1998'},
 178: {'Symbol': 'EQR', 'Security': 'Equity Residential', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Multi-Family Residential REITs','Date added': '2001-12-03','Founded': '1969'},
 179: {'Symbol': 'ESS', 'Security': 'Essex Property Trust', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Multi-Family Residential REITs','Date added': '2014-04-02','Founded': '1971'},
 180: {'Symbol': 'EL', 'Security': 'Estée Lauder Companies (The)', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Personal Care Products','Date added': '2006-01-05','Founded': '1946'},
 181: {'Symbol': 'ETSY', 'Security': 'Etsy', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Broadline Retail','Date added': '2020-09-21','Founded': '2005'},
 182: {'Symbol': 'EG', 'Security': 'Everest Re', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Reinsurance','Date added': '2017-06-19','Founded': '1973'},
 183: {'Symbol': 'EVRG', 'Security': 'Evergy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '2018-06-05','Founded': '1909'},
 184: {'Symbol': 'ES', 'Security': 'Eversource', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '2009-07-24','Founded': '1966'},
 185: {'Symbol': 'EXC', 'Security': 'Exelon', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '1957-03-04','Founded': '2000'},
 186: {'Symbol': 'EXPE', 'Security': 'Expedia Group', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Hotels, Resorts & Cruise Lines','Date added': '2007-10-02','Founded': '1996'},
 187: {'Symbol': 'EXPD', 'Security': 'Expeditors International', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Air Freight & Logistics','Date added': '2007-10-10','Founded': '1979'},
 188: {'Symbol': 'EXR', 'Security': 'Extra Space Storage', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Self-Storage REITs','Date added': '2016-01-19','Founded': '1977'},
 189: {'Symbol': 'XOM', 'Security': 'ExxonMobil', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Integrated Oil & Gas','Date added': '1957-03-04','Founded': '1999'},
 190: {'Symbol': 'FFIV', 'Security': 'F5, Inc.', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Communications Equipment','Date added': '2010-12-20','Founded': '1996'},
 191: {'Symbol': 'FDS', 'Security': 'FactSet', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '2021-12-20','Founded': '1978'},
 192: {'Symbol': 'FICO', 'Security': 'Fair Isaac', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '2023-03-20','Founded': '1956'},
 193: {'Symbol': 'FAST', 'Security': 'Fastenal', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Trading Companies & Distributors','Date added': '2008-09-15','Founded': '1967'},
 194: {'Symbol': 'FRT', 'Security': 'Federal Realty', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Retail REITs','Date added': '2016-02-01','Founded': '1962'},
 195: {'Symbol': 'FDX', 'Security': 'FedEx', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Air Freight & Logistics','Date added': '1980-12-31','Founded': '1971'},
 196: {'Symbol': 'FIS', 'Security': 'Fidelity National Information Services', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Transaction & Payment Processing Services','Date added': '2006-11-10','Founded': '1968'},
 197: {'Symbol': 'FITB', 'Security': 'Fifth Third Bank', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Diversified Banks','Date added': '1996-03-29','Founded': '1858'},
 198: {'Symbol': 'FSLR', 'Security': 'First Solar', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2022-12-19','Founded': '1999'},
 199: {'Symbol': 'FE', 'Security': 'FirstEnergy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '1997-11-28','Founded': '1997'},
 200: {'Symbol': 'FI', 'Security': 'Fiserv', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Transaction & Payment Processing Services','Date added': '2001-04-02','Founded': '1984'},
 201: {'Symbol': 'FMC', 'Security': 'FMC Corporation', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Fertilizers & Agricultural Chemicals','Date added': '2009-08-19','Founded': '1883'},
 202: {'Symbol': 'F', 'Security': 'Ford Motor Company', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Automobile Manufacturers','Date added': '1957-03-04','Founded': '1903'},
 203: {'Symbol': 'FTNT', 'Security': 'Fortinet', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Systems Software','Date added': '2018-10-11','Founded': '2000'},
 204: {'Symbol': 'FTV', 'Security': 'Fortive', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '2016-07-01','Founded': '2016'},
 205: {'Symbol': 'FOXA', 'Security': 'Fox Corporation (Class A)', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Broadcasting','Date added': '2019-03-04','Founded': '2019'},
 206: {'Symbol': 'FOX', 'Security': 'Fox Corporation (Class B)', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Broadcasting','Date added': '2019-03-04','Founded': '2019'},
 207: {'Symbol': 'BEN', 'Security': 'Franklin Templeton', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '1998-04-30','Founded': '1947'},
 208: {'Symbol': 'FCX', 'Security': 'Freeport-McMoRan', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Copper','Date added': '2011-07-01','Founded': '1912'},
 209: {'Symbol': 'GRMN', 'Security': 'Garmin', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Consumer Electronics','Date added': '2012-12-12','Founded': '1989'},
 210: {'Symbol': 'IT', 'Security': 'Gartner', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'IT Consulting & Other Services','Date added': '2017-04-05','Founded': '1979'},
 211: {'Symbol': 'GE', 'Security': 'GE Aerospace', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '1957-03-04','Founded': '1892'},
 212: {'Symbol': 'GEHC', 'Security': 'GE HealthCare', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2023-01-04','Founded': '1994'},
 213: {'Symbol': 'GEV', 'Security': 'GE Vernova', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Heavy Electrical Equipment','Date added': '2024-04-02','Founded': '2024'},
 214: {'Symbol': 'GEN', 'Security': 'Gen Digital', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Systems Software','Date added': '2003-03-25','Founded': '1982'},
 215: {'Symbol': 'GNRC', 'Security': 'Generac', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Electrical Components & Equipment','Date added': '2021-03-22','Founded': '1959'},
 216: {'Symbol': 'GD', 'Security': 'General Dynamics', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '1957-03-04','Founded': '1899'},
 217: {'Symbol': 'GIS', 'Security': 'General Mills', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '1957-03-04','Founded': '1856'},
 218: {'Symbol': 'GM', 'Security': 'General Motors', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Automobile Manufacturers','Date added': '2013-06-06','Founded': '1908'},
 219: {'Symbol': 'GPC', 'Security': 'Genuine Parts Company', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Distributors','Date added': '1973-12-31','Founded': '1925'},
 220: {'Symbol': 'GILD', 'Security': 'Gilead Sciences', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Biotechnology','Date added': '2004-07-01','Founded': '1987'},
 221: {'Symbol': 'GPN', 'Security': 'Global Payments', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Transaction & Payment Processing Services','Date added': '2016-04-25','Founded': '2000'},
 222: {'Symbol': 'GL', 'Security': 'Globe Life', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Life & Health Insurance','Date added': '1989-04-30','Founded': '1900'},
 223: {'Symbol': 'GDDY', 'Security': 'GoDaddy', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Internet Services & Infrastructure','Date added': '2024-06-24','Founded': '1997'},
 224: {'Symbol': 'GS', 'Security': 'Goldman Sachs', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Investment Banking & Brokerage','Date added': '2002-07-22','Founded': '1869'},
 225: {'Symbol': 'HAL', 'Security': 'Halliburton', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Equipment & Services','Date added': '1957-03-04','Founded': '1919'},
 226: {'Symbol': 'HIG', 'Security': 'Hartford (The)', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Property & Casualty Insurance','Date added': '1957-03-04','Founded': '1810'},
 227: {'Symbol': 'HAS', 'Security': 'Hasbro', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Leisure Products','Date added': '1984-09-30','Founded': '1923'},
 228: {'Symbol': 'HCA', 'Security': 'HCA Healthcare', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Facilities','Date added': '2015-01-27','Founded': '1968'},
 229: {'Symbol': 'DOC', 'Security': 'Healthpeak', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Health Care REITs','Date added': '2008-03-31','Founded': '1985'},
 230: {'Symbol': 'HSIC', 'Security': 'Henry Schein', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Distributors','Date added': '2015-03-17','Founded': '1932'},
 231: {'Symbol': 'HSY', 'Security': "Hershey's", 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '1957-03-04','Founded': '1894'},
 232: {'Symbol': 'HES', 'Security': 'Hess Corporation', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Integrated Oil & Gas','Date added': '1984-05-31','Founded': '1919'},
 233: {'Symbol': 'HPE', 'Security': 'Hewlett Packard Enterprise', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Technology Hardware, Storage & Peripherals','Date added': '2015-11-02','Founded': '2015'},
 234: {'Symbol': 'HLT', 'Security': 'Hilton Worldwide', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Hotels, Resorts & Cruise Lines','Date added': '2017-06-19','Founded': '1919'},
 235: {'Symbol': 'HOLX', 'Security': 'Hologic', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2016-03-30','Founded': '1985'},
 236: {'Symbol': 'HD', 'Security': 'Home Depot (The)', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Home Improvement Retail','Date added': '1988-03-31','Founded': '1978'},
 237: {'Symbol': 'HON', 'Security': 'Honeywell', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Conglomerates','Date added': '1957-03-04','Founded': '1906'},
 238: {'Symbol': 'HRL', 'Security': 'Hormel Foods', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '2009-03-04','Founded': '1891'},
 239: {'Symbol': 'HST', 'Security': 'Host Hotels & Resorts', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Hotel & Resort REITs','Date added': '2007-03-20','Founded': '1993'},
 240: {'Symbol': 'HWM', 'Security': 'Howmet Aerospace', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '2016-10-21','Founded': '1888'},
 241: {'Symbol': 'HPQ', 'Security': 'HP Inc.', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Technology Hardware, Storage & Peripherals','Date added': '1974-12-31','Founded': '1939 (2015)'},
 242: {'Symbol': 'HUBB', 'Security': 'Hubbell Incorporated', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '2023-10-18','Founded': '1888'},
 243: {'Symbol': 'HUM', 'Security': 'Humana', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Managed Health Care','Date added': '2012-12-10','Founded': '1961'},
 244: {'Symbol': 'HBAN', 'Security': 'Huntington Bancshares', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Regional Banks','Date added': '1997-08-28','Founded': '1866'},
 245: {'Symbol': 'HII', 'Security': 'Huntington Ingalls Industries', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '2018-01-03','Founded': '2011'},
 246: {'Symbol': 'IBM', 'Security': 'IBM', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'IT Consulting & Other Services','Date added': '1957-03-04','Founded': '1911'},
 247: {'Symbol': 'IEX', 'Security': 'IDEX Corporation', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '2019-08-09','Founded': '1988'},
 248: {'Symbol': 'IDXX', 'Security': 'Idexx Laboratories', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2017-01-05','Founded': '1983'},
 249: {'Symbol': 'ITW', 'Security': 'Illinois Tool Works', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '1986-02-28','Founded': '1912'},
 250: {'Symbol': 'INCY', 'Security': 'Incyte', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Biotechnology','Date added': '2017-02-28','Founded': '1991'},
 251: {'Symbol': 'IR', 'Security': 'Ingersoll Rand', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '2020-03-03','Founded': '1859'},
 252: {'Symbol': 'PODD', 'Security': 'Insulet Corporation', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2023-03-15','Founded': '2000'},
 253: {'Symbol': 'INTC', 'Security': 'Intel', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '1976-12-31','Founded': '1968'},
 254: {'Symbol': 'ICE', 'Security': 'Intercontinental Exchange', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '2007-09-26','Founded': '2000'},
 255: {'Symbol': 'IFF', 'Security': 'International Flavors & Fragrances', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '1976-03-31','Founded': '1958 (1889)'},
 256: {'Symbol': 'IP', 'Security': 'International Paper', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Paper & Plastic Packaging Products & Materials','Date added': '1957-03-04','Founded': '1898'},
 257: {'Symbol': 'IPG', 'Security': 'Interpublic Group of Companies (The)', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Advertising','Date added': '1992-10-01','Founded': '1961 (1930)'},
 258: {'Symbol': 'INTU', 'Security': 'Intuit', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '2000-12-05','Founded': '1983'},
 259: {'Symbol': 'ISRG', 'Security': 'Intuitive Surgical', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2008-06-02','Founded': '1995'},
 260: {'Symbol': 'IVZ', 'Security': 'Invesco', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '2008-08-21','Founded': '1935'},
 261: {'Symbol': 'INVH', 'Security': 'Invitation Homes', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Single-Family Residential REITs','Date added': '2022-09-19','Founded': '2012'},
 262: {'Symbol': 'IQV', 'Security': 'IQVIA', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '2017-08-29','Founded': '1982'},
 263: {'Symbol': 'IRM', 'Security': 'Iron Mountain', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Other Specialized REITs','Date added': '2009-01-06','Founded': '1951'},
 264: {'Symbol': 'JBHT', 'Security': 'J.B. Hunt', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Cargo Ground Transportation','Date added': '2015-07-01','Founded': '1961'},
 265: {'Symbol': 'JBL', 'Security': 'Jabil', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Manufacturing Services','Date added': '2023-12-18','Founded': '1966'},
 266: {'Symbol': 'JKHY', 'Security': 'Jack Henry & Associates', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Transaction & Payment Processing Services','Date added': '2018-11-13','Founded': '1976'},
 267: {'Symbol': 'J', 'Security': 'Jacobs Solutions', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Construction & Engineering','Date added': '2007-10-26','Founded': '1947'},
 268: {'Symbol': 'JNJ', 'Security': 'Johnson & Johnson', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Pharmaceuticals','Date added': '1973-06-30','Founded': '1886'},
 269: {'Symbol': 'JCI', 'Security': 'Johnson Controls', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Building Products','Date added': '2010-08-27','Founded': '1885'},
 270: {'Symbol': 'JPM', 'Security': 'JPMorgan Chase', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Diversified Banks','Date added': '1975-06-30','Founded': '2000 (1799 / 1871)'},
 271: {'Symbol': 'JNPR', 'Security': 'Juniper Networks', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Communications Equipment','Date added': '2006-06-02','Founded': '1996'},
 272: {'Symbol': 'K', 'Security': 'Kellanova', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '1989-09-11','Founded': '1906'},
 273: {'Symbol': 'KVUE', 'Security': 'Kenvue', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Personal Care Products','Date added': '2023-08-25','Founded': '2022 (Johnson & Johnson spinoff)'},
 274: {'Symbol': 'KDP', 'Security': 'Keurig Dr Pepper', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Soft Drinks & Non-alcoholic Beverages','Date added': '2022-06-21','Founded': '1981'},
 275: {'Symbol': 'KEY', 'Security': 'KeyCorp', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Regional Banks','Date added': '1994-03-01','Founded': '1825'},
 276: {'Symbol': 'KEYS', 'Security': 'Keysight', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Equipment & Instruments','Date added': '2018-11-06','Founded': '2014 (1939)'},
 277: {'Symbol': 'KMB', 'Security': 'Kimberly-Clark', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Household Products','Date added': '1957-03-04','Founded': '1872'},
 278: {'Symbol': 'KIM', 'Security': 'Kimco Realty', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Retail REITs','Date added': '2006-04-04','Founded': '1958'},
 279: {'Symbol': 'KMI', 'Security': 'Kinder Morgan', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Storage & Transportation','Date added': '2012-05-25','Founded': '1997'},
 280: {'Symbol': 'KKR', 'Security': 'KKR', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '2024-06-24','Founded': '1976'},
 281: {'Symbol': 'KLAC', 'Security': 'KLA Corporation', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductor Materials & Equipment','Date added': '1997-09-30','Founded': '1975/1977 (1997)'},
 282: {'Symbol': 'KHC', 'Security': 'Kraft Heinz', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '2015-07-06','Founded': '2015 (1869)'},
 283: {'Symbol': 'KR', 'Security': 'Kroger', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Food Retail','Date added': '1957-03-04','Founded': '1883'},
 284: {'Symbol': 'LHX', 'Security': 'L3Harris', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '2008-09-22','Founded': '2019 (L3 1997, Harris 1895)'},
 285: {'Symbol': 'LH', 'Security': 'LabCorp', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Services','Date added': '2004-11-01','Founded': '1978'},
 286: {'Symbol': 'LRCX', 'Security': 'Lam Research', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductor Materials & Equipment','Date added': '2012-06-29','Founded': '1980'},
 287: {'Symbol': 'LW', 'Security': 'Lamb Weston', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '2018-12-03','Founded': '2016 (1950)'},
 288: {'Symbol': 'LVS', 'Security': 'Las Vegas Sands', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Casinos & Gaming','Date added': '2019-10-03','Founded': '1988'},
 289: {'Symbol': 'LDOS', 'Security': 'Leidos', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Diversified Support Services','Date added': '2019-08-09','Founded': '1969'},
 290: {'Symbol': 'LEN', 'Security': 'Lennar', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Homebuilding','Date added': '2005-10-04','Founded': '1954'},
 291: {'Symbol': 'LIN', 'Security': 'Linde plc', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Industrial Gases','Date added': '1992-07-01','Founded': '1879'},
 292: {'Symbol': 'LYV', 'Security': 'Live Nation Entertainment', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Movies & Entertainment','Date added': '2019-12-23','Founded': '2010'},
 293: {'Symbol': 'LKQ', 'Security': 'LKQ Corporation', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Distributors','Date added': '2016-05-23','Founded': '1998'},
 294: {'Symbol': 'LMT', 'Security': 'Lockheed Martin', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '1957-03-04','Founded': '1995'},
 295: {'Symbol': 'L', 'Security': 'Loews Corporation', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Multi-line Insurance','Date added': '1995-05-31','Founded': '1959'},
 296: {'Symbol': 'LOW', 'Security': "Lowe's", 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Home Improvement Retail','Date added': '1984-02-29','Founded': '1904/1946/1959'},
 297: {'Symbol': 'LULU', 'Security': 'Lululemon Athletica', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Apparel, Accessories & Luxury Goods','Date added': '2023-10-18','Founded': '1998'},
 298: {'Symbol': 'LYB', 'Security': 'LyondellBasell', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '2012-09-05','Founded': '2007'},
 299: {'Symbol': 'MTB', 'Security': 'M&T Bank', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Regional Banks','Date added': '2004-02-23','Founded': '1856'},
 300: {'Symbol': 'MRO', 'Security': 'Marathon Oil', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '1957-03-04','Founded': '1887'},
 301: {'Symbol': 'MPC', 'Security': 'Marathon Petroleum', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Refining & Marketing','Date added': '2011-07-01','Founded': '2009 (1887)'},
 302: {'Symbol': 'MKTX', 'Security': 'MarketAxess', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '2019-07-01','Founded': '2000'},
 303: {'Symbol': 'MAR', 'Security': 'Marriott International', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Hotels, Resorts & Cruise Lines','Date added': '1998-05-29','Founded': '1927'},
 304: {'Symbol': 'MMC', 'Security': 'Marsh McLennan', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Insurance Brokers','Date added': '1987-08-31','Founded': '1905'},
 305: {'Symbol': 'MLM', 'Security': 'Martin Marietta Materials', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Construction Materials','Date added': '2014-07-02','Founded': '1993'},
 306: {'Symbol': 'MAS', 'Security': 'Masco', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Building Products','Date added': '1981-06-30','Founded': '1929'},
 307: {'Symbol': 'MA', 'Security': 'Mastercard', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Transaction & Payment Processing Services','Date added': '2008-07-18','Founded': '1966'},
 308: {'Symbol': 'MTCH', 'Security': 'Match Group', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Interactive Media & Services','Date added': '2021-09-20','Founded': '1986'},
 309: {'Symbol': 'MKC', 'Security': 'McCormick & Company', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '2003-03-20','Founded': '1889'},
 310: {'Symbol': 'MCD', 'Security': "McDonald's", 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Restaurants','Date added': '1970-06-30','Founded': '1940'},
 311: {'Symbol': 'MCK', 'Security': 'McKesson Corporation', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Distributors','Date added': '1999-01-13','Founded': '1833'},
 312: {'Symbol': 'MDT', 'Security': 'Medtronic', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '1986-10-31','Founded': '1949'},
 313: {'Symbol': 'MRK', 'Security': 'Merck & Co.', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Pharmaceuticals','Date added': '1957-03-04','Founded': '1891'},
 314: {'Symbol': 'META', 'Security': 'Meta Platforms', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Interactive Media & Services','Date added': '2013-12-23','Founded': '2004'},
 315: {'Symbol': 'MET', 'Security': 'MetLife', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Life & Health Insurance','Date added': '2000-12-11','Founded': '1868'},
 316: {'Symbol': 'MTD', 'Security': 'Mettler Toledo', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '2016-09-06','Founded': '1945'},
 317: {'Symbol': 'MGM', 'Security': 'MGM Resorts', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Casinos & Gaming','Date added': '2017-07-26','Founded': '1986'},
 318: {'Symbol': 'MCHP', 'Security': 'Microchip Technology', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2007-09-07','Founded': '1989'},
 319: {'Symbol': 'MU', 'Security': 'Micron Technology', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '1994-09-27','Founded': '1978'},
 320: {'Symbol': 'MSFT', 'Security': 'Microsoft', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Systems Software','Date added': '1994-06-01','Founded': '1975'},
 321: {'Symbol': 'MAA', 'Security': 'Mid-America Apartment Communities', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Multi-Family Residential REITs','Date added': '2016-12-02','Founded': '1977'},
 322: {'Symbol': 'MRNA', 'Security': 'Moderna', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Biotechnology','Date added': '2021-07-21','Founded': '2010'},
 323: {'Symbol': 'MHK', 'Security': 'Mohawk Industries', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Home Furnishings','Date added': '2013-12-23','Founded': '1878'},
 324: {'Symbol': 'MOH', 'Security': 'Molina Healthcare', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Managed Health Care','Date added': '2022-03-02','Founded': '1980'},
 325: {'Symbol': 'TAP', 'Security': 'Molson Coors Beverage Company', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Brewers','Date added': '1976-06-30','Founded': '2005 (Molson 1786, Coors 1873)'},
 326: {'Symbol': 'MDLZ', 'Security': 'Mondelez International', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '2012-10-02','Founded': '2012'},
 327: {'Symbol': 'MPWR', 'Security': 'Monolithic Power Systems', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2021-02-12','Founded': '1997'},
 328: {'Symbol': 'MNST', 'Security': 'Monster Beverage', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Soft Drinks & Non-alcoholic Beverages','Date added': '2012-06-28','Founded': '2012 (1935)'},
 329: {'Symbol': 'MCO', 'Security': "Moody's Corporation", 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '1998-07-01','Founded': '1909'},
 330: {'Symbol': 'MS', 'Security': 'Morgan Stanley', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Investment Banking & Brokerage','Date added': '1993-07-29','Founded': '1935'},
 331: {'Symbol': 'MOS', 'Security': 'Mosaic Company (The)', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Fertilizers & Agricultural Chemicals','Date added': '2011-09-26','Founded': '2004 (1865 / 1909)'},
 332: {'Symbol': 'MSI', 'Security': 'Motorola Solutions', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Communications Equipment','Date added': '1957-03-04','Founded': '1928 (2011)'},
 333: {'Symbol': 'MSCI', 'Security': 'MSCI', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '2018-04-04','Founded': '1969'},
 334: {'Symbol': 'NDAQ', 'Security': 'Nasdaq, Inc.', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '2008-10-22','Founded': '1971'},
 335: {'Symbol': 'NTAP', 'Security': 'NetApp', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Technology Hardware, Storage & Peripherals','Date added': '1999-06-25','Founded': '1992'},
 336: {'Symbol': 'NFLX', 'Security': 'Netflix', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Movies & Entertainment','Date added': '2010-12-20','Founded': '1997'},
 337: {'Symbol': 'NEM', 'Security': 'Newmont', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Gold','Date added': '1969-06-30','Founded': '1921'},
 338: {'Symbol': 'NWSA', 'Security': 'News Corp (Class A)', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Publishing','Date added': '2013-08-01','Founded': '2013 (News Corporation 1980)'},
 339: {'Symbol': 'NWS', 'Security': 'News Corp (Class B)', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Publishing','Date added': '2015-09-18','Founded': '2013 (News Corporation 1980)'},
 340: {'Symbol': 'NEE', 'Security': 'NextEra Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '1976-06-30','Founded': '1984 (1925)'},
 341: {'Symbol': 'NKE', 'Security': 'Nike, Inc.', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Apparel, Accessories & Luxury Goods','Date added': '1988-11-30','Founded': '1964'},
 342: {'Symbol': 'NI', 'Security': 'NiSource', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '2000-11-02','Founded': '1912'},
 343: {'Symbol': 'NDSN', 'Security': 'Nordson Corporation', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '2022-02-15','Founded': '1935'},
 344: {'Symbol': 'NSC', 'Security': 'Norfolk Southern Railway', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Rail Transportation','Date added': '1957-03-04','Founded': '1881/1894 (1980)'},
 345: {'Symbol': 'NTRS', 'Security': 'Northern Trust', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '1998-01-30','Founded': '1889'},
 346: {'Symbol': 'NOC', 'Security': 'Northrop Grumman', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '1957-03-04','Founded': '1994 (Northrop 1939, Grumman 1930)'},
 347: {'Symbol': 'NCLH', 'Security': 'Norwegian Cruise Line Holdings', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Hotels, Resorts & Cruise Lines','Date added': '2017-10-13','Founded': '2011 (1966)'},
 348: {'Symbol': 'NRG', 'Security': 'NRG Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Independent Power Producers & Energy Traders','Date added': '2010-01-29','Founded': '1992'},
 349: {'Symbol': 'NUE', 'Security': 'Nucor', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Steel','Date added': '1985-04-30','Founded': '1940'},
 350: {'Symbol': 'NVDA', 'Security': 'Nvidia', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2001-11-30','Founded': '1993'},
 351: {'Symbol': 'NVR', 'Security': 'NVR, Inc.', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Homebuilding','Date added': '2019-09-26','Founded': '1980'},
 352: {'Symbol': 'NXPI', 'Security': 'NXP Semiconductors', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2021-03-22','Founded': '1953'},
 353: {'Symbol': 'ORLY', 'Security': "O'Reilly Auto Parts", 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Automotive Retail','Date added': '2009-03-27','Founded': '1957'},
 354: {'Symbol': 'OXY', 'Security': 'Occidental Petroleum', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Exploration & Production','Date added': '1957-03-04','Founded': '1920'},
 355: {'Symbol': 'ODFL', 'Security': 'Old Dominion', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Cargo Ground Transportation','Date added': '2019-12-09','Founded': '1934'},
 356: {'Symbol': 'OMC', 'Security': 'Omnicom Group', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Advertising','Date added': '1997-12-31','Founded': '1986'},
 357: {'Symbol': 'ON', 'Security': 'ON Semiconductor', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2022-06-21','Founded': '1999'},
 358: {'Symbol': 'OKE', 'Security': 'ONEOK', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Storage & Transportation','Date added': '2010-03-15','Founded': '1906'},
 359: {'Symbol': 'ORCL', 'Security': 'Oracle Corporation', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '1989-08-31','Founded': '1977'},
 360: {'Symbol': 'OTIS', 'Security': 'Otis Worldwide', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '2020-04-03','Founded': '2020 (1853, United Technologies spinoff)'},
 361: {'Symbol': 'PCAR', 'Security': 'Paccar', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Construction Machinery & Heavy Transportation Equipment','Date added': '1980-12-31','Founded': '1905'},
 362: {'Symbol': 'PKG', 'Security': 'Packaging Corporation of America', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Paper & Plastic Packaging Products & Materials','Date added': '2017-07-26','Founded': '1959'},
 363: {'Symbol': 'PANW', 'Security': 'Palo Alto Networks', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Systems Software','Date added': '2023-06-20','Founded': '2005'},
 364: {'Symbol': 'PARA', 'Security': 'Paramount Global', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Movies & Entertainment','Date added': '1994-09-30','Founded': '2019 (Paramount Pictures 1912)'},
 365: {'Symbol': 'PH', 'Security': 'Parker Hannifin', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '1985-11-30','Founded': '1917'},
 366: {'Symbol': 'PAYX', 'Security': 'Paychex', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Human Resource & Employment Services','Date added': '1998-10-01','Founded': '1971'},
 367: {'Symbol': 'PAYC', 'Security': 'Paycom', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Human Resource & Employment Services','Date added': '2020-01-28','Founded': '1998'},
 368: {'Symbol': 'PYPL', 'Security': 'PayPal', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Transaction & Payment Processing Services','Date added': '2015-07-20','Founded': '1998'},
 369: {'Symbol': 'PNR', 'Security': 'Pentair', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '2012-10-01','Founded': '1966'},
 370: {'Symbol': 'PEP', 'Security': 'PepsiCo', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Soft Drinks & Non-alcoholic Beverages','Date added': '1957-03-04','Founded': '1898'},
 371: {'Symbol': 'PFE', 'Security': 'Pfizer', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Pharmaceuticals','Date added': '1957-03-04','Founded': '1849'},
 372: {'Symbol': 'PCG', 'Security': 'PG&E Corporation', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '2022-10-03','Founded': '1905'},
 373: {'Symbol': 'PM', 'Security': 'Philip Morris International', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Tobacco','Date added': '2008-03-31','Founded': '2008 (1847)'},
 374: {'Symbol': 'PSX', 'Security': 'Phillips 66', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Refining & Marketing','Date added': '2012-05-01','Founded': '2012 (1917)'},
 375: {'Symbol': 'PNW', 'Security': 'Pinnacle West', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '1999-10-04','Founded': '1985'},
 376: {'Symbol': 'PNC', 'Security': 'PNC Financial Services', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Regional Banks','Date added': '1988-04-30','Founded': '1845'},
 377: {'Symbol': 'POOL', 'Security': 'Pool Corporation', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Distributors','Date added': '2020-10-07','Founded': '1993'},
 378: {'Symbol': 'PPG', 'Security': 'PPG Industries', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '1957-03-04','Founded': '1883'},
 379: {'Symbol': 'PPL', 'Security': 'PPL Corporation', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '2001-10-01','Founded': '1920'},
 380: {'Symbol': 'PFG', 'Security': 'Principal Financial Group', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Life & Health Insurance','Date added': '2002-07-22','Founded': '1879'},
 381: {'Symbol': 'PG', 'Security': 'Procter & Gamble', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Personal Care Products','Date added': '1957-03-04','Founded': '1837'},
 382: {'Symbol': 'PGR', 'Security': 'Progressive Corporation', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Property & Casualty Insurance','Date added': '1997-08-04','Founded': '1937'},
 383: {'Symbol': 'PLD', 'Security': 'Prologis', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Industrial REITs','Date added': '2003-07-17','Founded': '1983'},
 384: {'Symbol': 'PRU', 'Security': 'Prudential Financial', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Life & Health Insurance','Date added': '2002-07-22','Founded': '1875'},
 385: {'Symbol': 'PEG', 'Security': 'Public Service Enterprise Group', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '1957-03-04','Founded': '1903'},
 386: {'Symbol': 'PTC', 'Security': 'PTC', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '2021-04-20','Founded': '1985'},
 387: {'Symbol': 'PSA', 'Security': 'Public Storage', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Self-Storage REITs','Date added': '2005-08-19','Founded': '1972'},
 388: {'Symbol': 'PHM', 'Security': 'PulteGroup', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Homebuilding','Date added': '1984-04-30','Founded': '1956'},
 389: {'Symbol': 'QRVO', 'Security': 'Qorvo', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2015-06-11','Founded': '2015'},
 390: {'Symbol': 'PWR', 'Security': 'Quanta Services', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Construction & Engineering','Date added': '2009-07-01','Founded': '1997'},
 391: {'Symbol': 'QCOM', 'Security': 'Qualcomm', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '1999-07-22','Founded': '1985'},
 392: {'Symbol': 'DGX', 'Security': 'Quest Diagnostics', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Services','Date added': '2002-12-12','Founded': '1967'},
 393: {'Symbol': 'RL', 'Security': 'Ralph Lauren Corporation', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Apparel, Accessories & Luxury Goods','Date added': '2007-02-02','Founded': '1967'},
 394: {'Symbol': 'RJF', 'Security': 'Raymond James', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Investment Banking & Brokerage','Date added': '2017-03-20','Founded': '1962'},
 395: {'Symbol': 'RTX', 'Security': 'RTX Corporation', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '1957-03-04','Founded': '1922'},
 396: {'Symbol': 'O', 'Security': 'Realty Income', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Retail REITs','Date added': '2015-04-07','Founded': '1969'},
 397: {'Symbol': 'REG', 'Security': 'Regency Centers', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Retail REITs','Date added': '2017-03-02','Founded': '1963'},
 398: {'Symbol': 'REGN', 'Security': 'Regeneron', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Biotechnology','Date added': '2013-05-01','Founded': '1988'},
 399: {'Symbol': 'RF', 'Security': 'Regions Financial Corporation', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Regional Banks','Date added': '1998-08-28','Founded': '1971'},
 400: {'Symbol': 'RSG', 'Security': 'Republic Services', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Environmental & Facilities Services','Date added': '2008-12-05','Founded': '1998 (1981)'},
 401: {'Symbol': 'RMD', 'Security': 'ResMed', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2017-07-26','Founded': '1989'},
 402: {'Symbol': 'RVTY', 'Security': 'Revvity', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '1985-05-31','Founded': '1937'},
 403: {'Symbol': 'ROK', 'Security': 'Rockwell Automation', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Electrical Components & Equipment','Date added': '2000-03-12','Founded': '1903'},
 404: {'Symbol': 'ROL', 'Security': 'Rollins, Inc.', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Environmental & Facilities Services','Date added': '2018-10-01','Founded': '1948'},
 405: {'Symbol': 'ROP', 'Security': 'Roper Technologies', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Equipment & Instruments','Date added': '2009-12-23','Founded': '1981'},
 406: {'Symbol': 'ROST', 'Security': 'Ross Stores', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Apparel Retail','Date added': '2009-12-21','Founded': '1982'},
 407: {'Symbol': 'RCL', 'Security': 'Royal Caribbean Group', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Hotels, Resorts & Cruise Lines','Date added': '2014-12-05','Founded': '1997'},
 408: {'Symbol': 'SPGI', 'Security': 'S&P Global', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Financial Exchanges & Data','Date added': '1957-03-04','Founded': '1917'},
 409: {'Symbol': 'CRM', 'Security': 'Salesforce', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '2008-09-15','Founded': '1999'},
 410: {'Symbol': 'SBAC', 'Security': 'SBA Communications', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Telecom Tower REITs','Date added': '2017-09-01','Founded': '1989'},
 411: {'Symbol': 'SLB', 'Security': 'Schlumberger', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Equipment & Services','Date added': '1957-03-04','Founded': '1926'},
 412: {'Symbol': 'STX', 'Security': 'Seagate Technology', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Technology Hardware, Storage & Peripherals','Date added': '2012-07-02','Founded': '1979'},
 413: {'Symbol': 'SRE', 'Security': 'Sempra Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '2017-03-17','Founded': '1998'},
 414: {'Symbol': 'NOW', 'Security': 'ServiceNow', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Systems Software','Date added': '2019-11-21','Founded': '2003'},
 415: {'Symbol': 'SHW', 'Security': 'Sherwin-Williams', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Specialty Chemicals','Date added': '1964-06-30','Founded': '1866'},
 416: {'Symbol': 'SPG', 'Security': 'Simon Property Group', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Retail REITs','Date added': '2002-06-26','Founded': '2003'},
 417: {'Symbol': 'SWKS', 'Security': 'Skyworks Solutions', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2015-03-12','Founded': '2002'},
 418: {'Symbol': 'SJM', 'Security': 'J.M. Smucker Company (The)', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '2008-11-06','Founded': '1897'},
 419: {'Symbol': 'SNA', 'Security': 'Snap-on', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '1982-09-30','Founded': '1920'},
 420: {'Symbol': 'SOLV', 'Security': 'Solventum', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Technology','Date added': '2024-04-01','Founded': '2023'},
 421: {'Symbol': 'SO', 'Security': 'Southern Company', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '1957-03-04','Founded': '1945'},
 422: {'Symbol': 'LUV', 'Security': 'Southwest Airlines', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Passenger Airlines','Date added': '1994-07-01','Founded': '1967'},
 423: {'Symbol': 'SWK', 'Security': 'Stanley Black & Decker', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '1982-09-30','Founded': '1843'},
 424: {'Symbol': 'SBUX', 'Security': 'Starbucks', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Restaurants','Date added': '2000-06-07','Founded': '1971'},
 425: {'Symbol': 'STT', 'Security': 'State Street Corporation', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '2003-03-14','Founded': '1792'},
 426: {'Symbol': 'STLD', 'Security': 'Steel Dynamics', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Steel','Date added': '2022-12-22','Founded': '1993'},
 427: {'Symbol': 'STE', 'Security': 'Steris', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2019-12-23','Founded': '1985'},
 428: {'Symbol': 'SYK', 'Security': 'Stryker Corporation', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2000-12-12','Founded': '1941'},
 429: {'Symbol': 'SMCI', 'Security': 'Supermicro', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Technology Hardware, Storage & Peripherals','Date added': '2024-03-18','Founded': '1993'},
 430: {'Symbol': 'SYF', 'Security': 'Synchrony Financial', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Consumer Finance','Date added': '2015-11-18','Founded': '2003'},
 431: {'Symbol': 'SNPS', 'Security': 'Synopsys', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '2017-03-16','Founded': '1986'},
 432: {'Symbol': 'SYY', 'Security': 'Sysco', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Food Distributors','Date added': '1986-12-31','Founded': '1969'},
 433: {'Symbol': 'TMUS', 'Security': 'T-Mobile US', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Wireless Telecommunication Services','Date added': '2019-07-15','Founded': '1994'},
 434: {'Symbol': 'TROW', 'Security': 'T. Rowe Price', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Asset Management & Custody Banks','Date added': '2019-07-29','Founded': '1937'},
 435: {'Symbol': 'TTWO', 'Security': 'Take-Two Interactive', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Interactive Home Entertainment','Date added': '2018-03-19','Founded': '1993'},
 436: {'Symbol': 'TPR', 'Security': 'Tapestry, Inc.', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Apparel, Accessories & Luxury Goods','Date added': '2004-09-01','Founded': '2017'},
 437: {'Symbol': 'TRGP', 'Security': 'Targa Resources', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Storage & Transportation','Date added': '2022-10-12','Founded': '2005'},
 438: {'Symbol': 'TGT', 'Security': 'Target Corporation', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Consumer Staples Merchandise Retail','Date added': '1976-12-31','Founded': '1902'},
 439: {'Symbol': 'TEL', 'Security': 'TE Connectivity', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Manufacturing Services','Date added': '2011-10-17','Founded': '2007'},
 440: {'Symbol': 'TDY', 'Security': 'Teledyne Technologies', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Equipment & Instruments','Date added': '2020-06-22','Founded': '1960'},
 441: {'Symbol': 'TFX', 'Security': 'Teleflex', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2019-01-18','Founded': '1943'},
 442: {'Symbol': 'TER', 'Security': 'Teradyne', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductor Materials & Equipment','Date added': '2020-09-21','Founded': '1960'},
 443: {'Symbol': 'TSLA', 'Security': 'Tesla, Inc.', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Automobile Manufacturers','Date added': '2020-12-21','Founded': '2003'},
 444: {'Symbol': 'TXN', 'Security': 'Texas Instruments', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Semiconductors','Date added': '2001-03-12','Founded': '1930'},
 445: {'Symbol': 'TXT', 'Security': 'Textron', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '1978-12-31','Founded': '1923'},
 446: {'Symbol': 'TMO', 'Security': 'Thermo Fisher Scientific', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '2004-08-03','Founded': '2006 (1902)'},
 447: {'Symbol': 'TJX', 'Security': 'TJX Companies', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Apparel Retail','Date added': '1985-09-30','Founded': '1987'},
 448: {'Symbol': 'TSCO', 'Security': 'Tractor Supply', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Other Specialty Retail','Date added': '2014-01-24','Founded': '1938'},
 449: {'Symbol': 'TT', 'Security': 'Trane Technologies', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Building Products','Date added': '2010-11-17','Founded': '1871'},
 450: {'Symbol': 'TDG', 'Security': 'TransDigm Group', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Aerospace & Defense','Date added': '2016-06-03','Founded': '1993'},
 451: {'Symbol': 'TRV', 'Security': 'Travelers Companies (The)', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Property & Casualty Insurance','Date added': '2002-08-21','Founded': '1853'},
 452: {'Symbol': 'TRMB', 'Security': 'Trimble Inc.', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Equipment & Instruments','Date added': '2021-01-21','Founded': '1978'},
 453: {'Symbol': 'TFC', 'Security': 'Truist', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Regional Banks','Date added': '1997-12-04','Founded': '1872'},
 454: {'Symbol': 'TYL', 'Security': 'Tyler Technologies', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Application Software','Date added': '2020-06-22','Founded': '1966'},
 455: {'Symbol': 'TSN', 'Security': 'Tyson Foods', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Packaged Foods & Meats','Date added': '2005-08-10','Founded': '1935'},
 456: {'Symbol': 'USB', 'Security': 'U.S. Bank', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Diversified Banks','Date added': '1999-11-01','Founded': '1968'},
 457: {'Symbol': 'UBER', 'Security': 'Uber', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Passenger Ground Transportation','Date added': '2023-12-18','Founded': '2009'},
 458: {'Symbol': 'UDR', 'Security': 'UDR, Inc.', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Multi-Family Residential REITs','Date added': '2016-03-07','Founded': '1972'},
 459: {'Symbol': 'ULTA', 'Security': 'Ulta Beauty', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Other Specialty Retail','Date added': '2016-04-18','Founded': '1990'},
 460: {'Symbol': 'UNP', 'Security': 'Union Pacific Corporation', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Rail Transportation','Date added': '1957-03-04','Founded': '1862'},
 461: {'Symbol': 'UAL', 'Security': 'United Airlines Holdings', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Passenger Airlines','Date added': '2015-09-03','Founded': '1967'},
 462: {'Symbol': 'UPS', 'Security': 'United Parcel Service', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Air Freight & Logistics','Date added': '2002-07-22','Founded': '1907'},
 463: {'Symbol': 'URI', 'Security': 'United Rentals', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Trading Companies & Distributors','Date added': '2014-09-20','Founded': '1997'},
 464: {'Symbol': 'UNH', 'Security': 'UnitedHealth Group', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Managed Health Care','Date added': '1994-07-01','Founded': '1977'},
 465: {'Symbol': 'UHS', 'Security': 'Universal Health Services', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Facilities','Date added': '2014-09-20','Founded': '1979'},
 466: {'Symbol': 'VLO', 'Security': 'Valero Energy', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Refining & Marketing','Date added': '2002-12-20','Founded': '1980'},
 467: {'Symbol': 'VTR', 'Security': 'Ventas', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Health Care REITs','Date added': '2009-03-04','Founded': '1998'},
 468: {'Symbol': 'VLTO', 'Security': 'Veralto', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Environmental & Facilities Services','Date added': '2023-10-02','Founded': '2023'},
 469: {'Symbol': 'VRSN', 'Security': 'Verisign', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Internet Services & Infrastructure','Date added': '2006-02-01','Founded': '1995'},
 470: {'Symbol': 'VRSK', 'Security': 'Verisk', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Research & Consulting Services','Date added': '2015-10-08','Founded': '1971'},
 471: {'Symbol': 'VZ', 'Security': 'Verizon', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Integrated Telecommunication Services','Date added': '1983-11-30','Founded': '1983 (1877)'},
 472: {'Symbol': 'VRTX', 'Security': 'Vertex Pharmaceuticals', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Biotechnology','Date added': '2013-09-23','Founded': '1989'},
 473: {'Symbol': 'VTRS', 'Security': 'Viatris', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Pharmaceuticals','Date added': '2004-04-23','Founded': '1961'},
 474: {'Symbol': 'VICI', 'Security': 'Vici Properties', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Hotel & Resort REITs','Date added': '2022-06-08','Founded': '2017'},
 475: {'Symbol': 'V', 'Security': 'Visa Inc.', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Transaction & Payment Processing Services','Date added': '2009-12-21','Founded': '1958'},
 476: {'Symbol': 'VST', 'Security': 'Vistra', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '2024-05-08','Founded': '2016'},
 477: {'Symbol': 'VMC', 'Security': 'Vulcan Materials Company', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Construction Materials','Date added': '1999-06-30','Founded': '1909'},
 478: {'Symbol': 'WRB', 'Security': 'W. R. Berkley Corporation', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Property & Casualty Insurance','Date added': '2019-12-05','Founded': '1967'},
 479: {'Symbol': 'GWW', 'Security': 'W. W. Grainger', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '1981-06-30','Founded': '1927'},
 480: {'Symbol': 'WAB', 'Security': 'Wabtec', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Construction Machinery & Heavy Transportation Equipment','Date added': '2019-02-27','Founded': '1999 (1869)'},
 481: {'Symbol': 'WBA', 'Security': 'Walgreens Boots Alliance', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Drug Retail','Date added': '1979-12-31','Founded': '2014'},
 482: {'Symbol': 'WMT', 'Security': 'Walmart', 'GICS Sector': 'Consumer Staples', 'GICS Sub-Industry': 'Consumer Staples Merchandise Retail','Date added': '1982-08-31','Founded': '1962'},
 483: {'Symbol': 'DIS', 'Security': 'Walt Disney Company (The)', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Movies & Entertainment','Date added': '1976-06-30','Founded': '1923'},
 484: {'Symbol': 'WBD', 'Security': 'Warner Bros. Discovery', 'GICS Sector': 'Communication Services', 'GICS Sub-Industry': 'Broadcasting','Date added': '2022-04-11','Founded': '2022 (Warner Bros. 1923)'},
 485: {'Symbol': 'WM', 'Security': 'Waste Management', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Environmental & Facilities Services','Date added': '1998-08-31','Founded': '1968'},
 486: {'Symbol': 'WAT', 'Security': 'Waters Corporation', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Life Sciences Tools & Services','Date added': '2002-01-02','Founded': '1958'},
 487: {'Symbol': 'WEC', 'Security': 'WEC Energy Group', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Electric Utilities','Date added': '2008-10-31','Founded': '1896'},
 488: {'Symbol': 'WFC', 'Security': 'Wells Fargo', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Diversified Banks','Date added': '1976-06-30','Founded': '1852'},
 489: {'Symbol': 'WELL', 'Security': 'Welltower', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Health Care REITs','Date added': '2009-01-30','Founded': '1970'},
 490: {'Symbol': 'WST', 'Security': 'West Pharmaceutical Services', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Supplies','Date added': '2020-05-22','Founded': '1923'},
 491: {'Symbol': 'WDC', 'Security': 'Western Digital', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Technology Hardware, Storage & Peripherals','Date added': '2009-07-01','Founded': '1970'},
 492: {'Symbol': 'WRK', 'Security': 'WestRock', 'GICS Sector': 'Materials', 'GICS Sub-Industry': 'Paper & Plastic Packaging Products & Materials','Date added': '2015-06-25','Founded': '2015'},
 493: {'Symbol': 'WY', 'Security': 'Weyerhaeuser', 'GICS Sector': 'Real Estate', 'GICS Sub-Industry': 'Timber REITs','Date added': '1979-10-01','Founded': '1900'},
 494: {'Symbol': 'WMB', 'Security': 'Williams Companies', 'GICS Sector': 'Energy', 'GICS Sub-Industry': 'Oil & Gas Storage & Transportation','Date added': '1975-03-31','Founded': '1908'},
 495: {'Symbol': 'WTW', 'Security': 'Willis Towers Watson', 'GICS Sector': 'Financials', 'GICS Sub-Industry': 'Insurance Brokers','Date added': '2016-01-05','Founded': '2016'},
 496: {'Symbol': 'WYNN', 'Security': 'Wynn Resorts', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Casinos & Gaming','Date added': '2008-11-14','Founded': '2002'},
 497: {'Symbol': 'XEL', 'Security': 'Xcel Energy', 'GICS Sector': 'Utilities', 'GICS Sub-Industry': 'Multi-Utilities','Date added': '1957-03-04','Founded': '1909'},
 498: {'Symbol': 'XYL', 'Security': 'Xylem Inc.', 'GICS Sector': 'Industrials', 'GICS Sub-Industry': 'Industrial Machinery & Supplies & Components','Date added': '2011-11-01','Founded': '2011'},
 499: {'Symbol': 'YUM', 'Security': 'Yum! Brands', 'GICS Sector': 'Consumer Discretionary', 'GICS Sub-Industry': 'Restaurants','Date added': '1997-10-06','Founded': '1997'},
 500: {'Symbol': 'ZBRA', 'Security': 'Zebra Technologies', 'GICS Sector': 'Information Technology', 'GICS Sub-Industry': 'Electronic Equipment & Instruments','Date added': '2019-12-23','Founded': '1969'},
 501: {'Symbol': 'ZBH', 'Security': 'Zimmer Biomet', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Health Care Equipment','Date added': '2001-08-07','Founded': '1927'},
 502: {'Symbol': 'ZTS', 'Security': 'Zoetis', 'GICS Sector': 'Health Care', 'GICS Sub-Industry': 'Pharmaceuticals','Date added': '2013-06-21','Founded': '1952'}}

ss.dfSP500 = pd.DataFrame(ss.dictSP500).T

ss.listSector = ss.dfSP500["GICS Sector"].unique()
# listSector

ss.dictIndustry = {}
for sector in ss.listSector:
    ss.dictIndustry[sector] = ss.dfSP500.loc[ss.dfSP500["GICS Sector"] == sector, "GICS Sub-Industry"].unique()
    ss.dictIndustry[sector] = np.insert(ss.dictIndustry[sector], 0, "All")
  
# =============================================================================================================
# SIDEBAR
choose = option_menu("Trade Screener", ["Summary", "Rubric"],
                                  # icons=["graph-up-arrow", "table", "grid-fill", "person-fill"],
                                  icons=["graph-up-arrow", "table", "grid-fill"],
                              menu_icon="calendar2-check", default_index=0, orientation = "horizontal",
                              styles={
    "container"         : {"padding": "5!important", "background-color": secondaryBackgroundColor},
    "icon"              : {"color": textColor, "font-size": "16px"}, 
    "nav-link"          : {"font-size": "12px", "text-align": "left", "margin":"0px", "--hover-color": colorLightPink},
    "nav-link-selected" : {"background-color": primaryColor},
}
)

# =============================================================================================================
# FUNCTIONS 
class TradingCalendar(AbstractHolidayCalendar):
    rule = [
        Holiday("NewYearsDay", month = 1, day = 1, observance = nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay, 
        GoodFriday,
        USMemorialDay,
        Holiday("Juneteenth", month = 6, day = 19, observance = nearest_workday),
        Holiday("Independence Day", month = 7, day = 4, observance = nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday("Christmas", month = 12, day = 25, observance = nearest_workday),
    ]

def createListTradingDays(dateStart, dateEnd):
    inst = TradingCalendar()
    holidays = inst.holidays(dateStart, dateEnd)
    listTradingDays = []
    # countTradingDays = 0
    
    for n in range(int((dateEnd - dateStart).days) + 1):
        date = dateStart + dt.timedelta(n)
        if int(date.isoweekday()) <= 5 and date not in holidays:
            listTradingDays.append(date)
    return listTradingDays

    # Example
    # listTradingDays = createListTradingDays(dateStart = datetime(2025, 1,1), dateEnd = datetime (2025, 12, 31))
    # st.write(listTradingDays)

def pad0(string):
    string = str(string)
    if len(string) < 2:
        strpad = "0" + string
    else:
        strpad = string
    return strpad

def changeRowBG(s, index_name):
    return ["background-color: lightgrey" if index_name in s.name else "" for _ in s]
    # Example
    # dfTest.style.apply(changeRowBG, index_name = "SUM", axis = 1).format("{:.0f}", height = heightTable)

# =============================================================================================================
# PROGRAM 
ss.nameTickerTextInput = 'AAPL'

# =============================================================================================================
# PAGE
if choose == "Documentation": 
    with st.expander('Home', expanded = True):
        st.subheader('Shiller PE Ratio')
        st.write('Shiller PE ratio for the S&P 500. Price earnings ratio is based on average inflation-adjusted earnings from the previous 10 years, known as the Cyclically Adjusted PE Ratio (CAPE Ratio), Shiller PE Ratio, or PE 10 FAQ. Data courtesy of Robert Shiller from his book, Irrational Exuberance.')
        st.caption('https://data.nasdaq.com/data/MULTPL/SHILLER_PE_RATIO_MONTH-shiller-pe-ratio-by-month')

# =============================================================================================================
# PAGE
if choose == "Rubric":
    with st.expander("Inputs:", expanded = True):
        # Create list of ticker
        cols = st.columns([4,4,1,3])
        nameSector = cols[0].selectbox("Sector", ss.listSector)
        nameIndustry = cols[1].selectbox("Industry", ss.dictIndustry[nameSector])
        if nameIndustry == "All":
            ss.listTicker = ss.dfSP500.loc[ss.dfSP500["GICS Sector"] == nameSector, "Symbol"]
            ss.dfTicker = ss.dfSP500[ss.dfSP500["GICS Sector"] == nameSector]
        else:
            ss.listTicker = ss.dfSP500.loc[ss.dfSP500["GICS Sub-Industry"] == nameIndustry, "Symbol"]
            ss.dfTicker = ss.dfSP500[ss.dfSP500["GICS Sub-Industry"] == nameIndustry]
        
        boolMAG7 = cols[2].button("MAG7")
        if boolMAG7:
            ss.listTicker = ["GOOGL", "AMZN", "AAPL", "META", "MSFT", "NVDA", "TSLA"]
        
        st.write("Company List (" , str(len(ss.dfTicker)) , " companies): ")
        ss.dfTicker

        listTicker = st.multiselect("Ticker", ss.listTicker, ss.listTicker)
        
        try: 
            ss.datac = yf.Tickers(" ".join(listTicker))
        except:
            listTicker = ss.listTicker 
            ss.datac = yf.Tickers(" ".join(listTicker))
        dfDataInfo_Scrape      = pd.DataFrame()
        # Create dataframe from info
        for nameTicker in listTicker:
            tempDataInfo     = convertyfinfo2df(ss.datac.tickers[nameTicker].info, dictDataInfoParams)
            dfDataInfo_Scrape = pd.concat([dfDataInfo_Scrape, tempDataInfo])
            
        # Set Index
        dfDataInfo_Scrape = dfDataInfo_Scrape.set_index("symbol")

        def convertName(list, dict):
            newlist = []
            for item in list:
                newlist.append(dict[item])
            return newlist

        def highlight(x):
            color_codes = pd.DataFrame("", index = x.index, columns = x.columns)
            color_codes.loc["PEG (<1)",:]             = np.where(np.logical_and(x.loc["PEG (<1)",:] > 0,x.loc["PEG (<1)",:] < 1), 'color:green', 'color:red')
            color_codes.loc["ROE/PBV (>5)",:]         = np.where(x.loc["ROE/PBV (>5)",:] > 5, 'color:green', 'color:red')
            color_codes.loc["QuickRatio (>1)",:]      = np.where(x.loc["QuickRatio (>1)",:] > 1 , 'color:green', 'color:red')
            color_codes.loc["ForwardPE",:]            = np.where(np.logical_and(x.loc["ForwardPE",:] > 0,x.loc["ForwardPE",:] < 20), 'color:green', 'color:red')
            color_codes.loc["Target High (%)",:]      = np.where(x.loc["Target High (%)",:] > 0, 'color:green', 'color:red')
            color_codes.loc["Target Median (%)",:]    = np.where(x.loc["Target Median (%)",:] > 0, 'color:green', 'color:red')
            color_codes.loc["Target Low (%)",:]       = np.where(x.loc["Target Low (%)",:] > 0, 'color:green', 'color:red')
            color_codes.loc["52wks High Chg (%)",:]   = np.where(x.loc["52wks High Chg (%)",:] > 0, 'color:green', 'color:red')
            color_codes.loc["52wks Low Chg (%)",:]    = np.where(x.loc["52wks Low Chg (%)",:] > 0, 'color:green', 'color:red')
            color_codes.loc["Revenue Growth (%)",:]   = np.where(x.loc["Revenue Growth (%)",:] > 5, 'color:green', 'color:red')
            color_codes.loc["Earnings Growth (%)",:]  = np.where(x.loc["Earnings Growth (%)",:] > 5, 'color:green', 'color:red')
            return color_codes
                
        # List Parameters
        listParam_Price   = ["currentPrice", "fiftyDayAverage", "twoHundredDayAverage", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "targetHighPrice", "targetMedianPrice","targetLowPrice"]
        listParam_Percent = ["fiftyTwoWeekHigh_(pct)", "fiftyTwoWeekLow_(pct)", "targetHigh_(pct)", "targetMedian_(pct)","targetLow_(pct)", "revenueGrowth_(pct)", "earningsGrowth_(pct)", "grossMargins_(pct)", "profitMargins_(pct)"]    
        listParam_Color   = ["pegRatio", "ROEPBV", "quickRatio", "forwardPE"]
        listParam_Other   = ["payoutRatio", "shortRatio","priceToBook","dividendYield_(pct)","returnOnAssets_(pct)", "returnOnEquity_(pct)"]
        listParam_Company = ["marketCap_(B)", "enterpriseValue_(B)", "totalRevenue_(B)", "grossProfits_(B)", "freeCashflow_(B)", "totalCash_(M)","totalDebt_(M)", "fullTimeEmployees", "heldPercentInsiders", "numberOfAnalystOpinions"]
                
        listParam       = listParam_Company + listParam_Price + listParam_Percent + listParam_Color + listParam_Other 
        listParam_Clean = convertName(listParam, dictShortName)

        listBackground = listParam_Price + listParam_Percent + listParam_Company
        listBackground_Clean  = convertName(listBackground, dictShortName)
        listBackground_Clean = ["Price ($)", "Revenue Growth (%)", "Earnings Growth (%)"]

        # Dataframe
        st.dataframe(dfDataInfo_Scrape[listParam].rename(columns = dictShortName).T.style.apply(lambda x: ['background-color: lightgrey' 
                                    if x.name in listBackground_Clean else '' for i in x], axis=1).apply(highlight, axis = None).format('{:,.2f}'), use_container_width = True, height = 1200)


if choose == "Summary":

    timetrack['start_analysis'] = np.round(time.time() - time_start)

    ss.boolLoadFromTextInput    = False
    ss.boolLoadFromSelectbox    = False

  #===================================================================================
  # User Input 
    with st.sidebar:
    
        with st.expander('Enter Ticker:', expanded = True):
            ss.nameTickerTextInput = st.text_input("", value = ss.nameTickerTextInput, key = 'keytextinput', help = "Use Yahoo Finance format such as Example: 'AAPL', '^DJI', 'LUNA1-USD', 'CL=F', 'PTT.BK")

        # Load Data
        ss.nameTicker = ss.nameTickerTextInput
        ss.data = yf.Ticker(ss.nameTicker)
        ss.dfDataAnalysis = convertyfinfo2df(ss.data.info, dictDataInfoParams, keyKeep = 'keepAnalysisPg')

    count = 0 

    # Check if the data is valid 
    try:
        ss.typeTicker = ss.dfDataAnalysis.loc[count,"quoteType"]
        ss.validTicker = True
    except:
        ss.validTicker = False

    timetrack['load_yfdata'] = np.round(time.time() - time_start)

  # #===================================================================================
  # # Save query in the dataframe
  # if ss.nameTicker != ss.nameTicker_init:
  #   ss.boolAggregateColumn  = False
  #   try:
  #     shortname = ss.dfDataAnalysis.loc[count,"shortName"]
  #     # Save query in google sheet
  #     ct = datetime.now()
  #     ts = ct.timestamp()
  #     nrow = ss.sheet_access_log_individual.rows
  #     ss.sheet_access_log_individual.insert_rows(nrow, values = [str(ct), ts, ss.ip_address, ss.nameTicker.upper()], inherit = True)

  #     # Save query
  #     ss.nameTicker_init = ss.nameTicker.upper()
  #   except:
  #     pass

  #===================================================================================
  # Sidebar
    with st.sidebar:

        # Estimates ----------------------------------------------------------------------
        try:
            if ss.typeTicker == 'EQUITY':
                with st.expander("Analyst Estimates for "+ ss.nameTicker + ":", expanded = True):
                    st.caption("No. Analysts: "+ str(ss.dfDataAnalysis.loc[count,"numberOfAnalystOpinions"]) + ' - ' + ss.dfDataAnalysis.loc[count,"recommendationKey"])
                    st.caption("Low: " + str(ss.dfDataAnalysis.loc[count,"targetLowPrice"]) + " / Median: " + str(ss.dfDataAnalysis.loc[count,"targetMedianPrice"]) + " / High: " + str(ss.dfDataAnalysis.loc[count,"targetHighPrice"]))
                    st.caption("52Wks Low: " + str(ss.dfDataAnalysis.loc[count,"fiftyTwoWeekLow"]) + " / 52Wks High: " + str(ss.dfDataAnalysis.loc[count,"fiftyTwoWeekHigh"]) )
                    st.caption("Cash per share " + str(ss.dfDataAnalysis.loc[count,"totalCashPerShare"]) + ' / ' + "Revenue per share " + str(ss.dfDataAnalysis.loc[count,"revenuePerShare"]))
            else:
                with st.expander("Price Range", expanded = True):    
                    st.caption("52Wks Low: " + str(ss.dfDataAnalysis.loc[count,"fiftyTwoWeekLow"]) + " / 52Wks High: " + str(ss.dfDataAnalysis.loc[count,"fiftyTwoWeekHigh"]) )
        except:
            pass
        
        timetrack['load analyst'] = np.round(time.time() - time_start)
      

        # Latest News ----------------------------------------------------------------------
        with st.expander('Latest News for '+ ss.nameTicker + ':', expanded = True):
            try: 
                for iNew in range(len(ss.data.news)):
                    title       = ss.data.news[iNew]['content']['title']
                    url         = ss.data.news[iNew]['content']['clickThroughUrl']['url']
                    publisher   = ss.data.news[iNew]['content']['provider']['displayName']
                    publishTime = ss.data.news[iNew]['content']['displayTime']
                    st.write("[%s](%s)" % (title + ' (' + publisher +  ')' , url))
                    st.caption(publishTime)
            except:
                pass
        timetrack['load news'] = np.round(time.time() - time_start)
        
    #===================================================================================
    # Program
    if not ss.validTicker:
        st.error( ss.nameTicker.upper() + ' is invalid Ticker. Please input valid ticker or search from company name.')
    else:
        
        timetrack['load price (init)'] = np.round(time.time() - time_start)
        # Header
        col1, col2, col3 = st.columns([4, 1, 2])
        col1.title(ss.dfDataAnalysis.loc[count,"shortName"])

        timetrack['load price (shortname)'] = np.round(time.time() - time_start)
        try:
            col2.image(ss.dfDataAnalysis.loc[count,"logo_url"])
        except:
            pass

        timetrack['load price (logo)'] = np.round(time.time() - time_start)
        try:
            dfPrice = ss.data.history(period='1mo')
            currentPrice = dfPrice['Close'][-1]
            previousPrice = dfPrice['Close'][-2]
            ss.pctChangePrice = (currentPrice - previousPrice)/previousPrice*100
            ss.currentPrice   = currentPrice
            if ss.pctChangePrice > 0:
                col3.metric("Price", np.round(currentPrice, decimals = 2), delta = '+' + str(np.round(ss.pctChangePrice, decimals = 2)) + '%')
            else:
                col3.metric("Price", np.round(currentPrice, decimals = 2), delta = str(np.round(ss.pctChangePrice, decimals = 2)) + '%')

        except:
            pass
        timetrack['load price (calc)'] = np.round(time.time() - time_start)

        try:
            if ss.dfDataAnalysis.loc[count,"website"] != np.nan:
                st.write(ss.dfDataAnalysis.loc[count,"website"])
        except:
            pass
        
        try:
            st.write('Twitter: ' + ss.dfDataAnalysis.loc[count,"twitter"])
        except:
            pass
    
        timetrack['load price (website)'] = np.round(time.time() - time_start)

        if ss.typeTicker == 'EQUITY':
        # The Numbers --------------------------------------------------------------------
            with st.expander("The Numbers:", expanded = True):
                # Description Table
                # st.write("The big numbers")
                col1, col2, col3, col4, col5 = st.columns(5)  
                col1.metric("Market Cap (B)",         ss.dfDataAnalysis.loc[count,"marketCap_(B)"].round(2))
                col2.metric("Enterprise (B)",         ss.dfDataAnalysis.loc[count,"enterpriseValue_(B)"].round(2))
                col3.metric("Revenue (B)",            ss.dfDataAnalysis.loc[count,"totalRevenue_(B)"].round(2))
                col4.metric("Gross Profit (B)",       ss.dfDataAnalysis.loc[count,"grossProfits_(B)"].round(2))
                col5.metric("Free Cash Flow (B)",     ss.dfDataAnalysis.loc[count,"freeCashflow_(B)"].round(2))

                # st.write("Ratio") 
                col1, col2, col3, col4, col5 = st.columns(5)  
                if np.logical_and(ss.dfDataAnalysis.loc[count,"pegRatio"] < 1,ss.dfDataAnalysis.loc[count,"pegRatio"] > 0):
                    col1.metric("PEG",           ss.dfDataAnalysis.loc[count,"pegRatio"], delta = '✓ 0 < PEG < 1')
                else:
                    col1.metric("PEG",           ss.dfDataAnalysis.loc[count,"pegRatio"], delta = '☓ PEG > 1 or < 0', delta_color = 'inverse')
                
                if ss.dfDataAnalysis.loc[count,"ROEPBV"] > 5:
                    col2.metric("ROE/PBV",       ss.dfDataAnalysis.loc[count,"ROEPBV"], delta = '✓ ROE/PBV > 5')
                else:
                    col2.metric("ROE/PBV",       ss.dfDataAnalysis.loc[count,"ROEPBV"], delta = '☓ ROE/PBV < 5', delta_color = 'inverse')
                
                if ss.dfDataAnalysis.loc[count,"quickRatio"] > 1:
                    col3.metric("Quick Ratio",   ss.dfDataAnalysis.loc[count,"quickRatio"], delta = '✓ Ratio > 1') 
                else:
                    col3.metric("Quick Ratio",   ss.dfDataAnalysis.loc[count,"quickRatio"], delta = '☓ Ratio < 1', delta_color = 'inverse') 
                    col4.metric("Payout Ratio",       ss.dfDataAnalysis.loc[count,"payoutRatio"])
                    col5.metric("Short Ratio",        ss.dfDataAnalysis.loc[count,"shortRatio"])
                    
                    # st.write("Value")
                    col1, col2, col3, col4, col5 = st.columns(5)  
                    col1.metric("Forward PE",         ss.dfDataAnalysis.loc[count,"forwardPE"])
                    col2.metric("PBV",                ss.dfDataAnalysis.loc[count,"priceToBook"])
                    col3.metric("DIV Yield (%)",      ss.dfDataAnalysis.loc[count,"dividendYield_(pct_str)"])
                    col4.metric("ROA (%)",            ss.dfDataAnalysis.loc[count,"returnOnAssets_(pct_str)"])
                    col5.metric("ROE (%)",            ss.dfDataAnalysis.loc[count,"returnOnEquity_(pct_str)"])

                    # st.write("Margin & Growth")
                    col1, col2, col3, col4, col5 = st.columns(5)  
                    col1.metric("Gross Margins",     ss.dfDataAnalysis.loc[count,"grossMargins_(pct_str)"])
                    col2.metric("Operating Margins", ss.dfDataAnalysis.loc[count,"operatingMargins_(pct_str)"])
                    col3.metric("Profit Margins",    ss.dfDataAnalysis.loc[count,"profitMargins_(pct_str)"])
                    col4.metric("Revenue Growth",    ss.dfDataAnalysis.loc[count,"revenueGrowth_(pct_str)"])
                    col5.metric("Earning Growth",    ss.dfDataAnalysis.loc[count,"earningsGrowth_(pct_str)"])
            
        timetrack['load numbers'] = np.round(time.time() - time_start)
    #===================================================================================
    with st.expander("Historical Price:", expanded = True):

        # User Inputs
        cols = st.columns(4)
        namePeriod = cols[0].selectbox("Time Interval:", options = ['1mo', '3mo', '6mo', '1y', '3y', '5y', 'ytd','max'], index = 4 )
        nSMA1      = cols[1].number_input('SMA Short', value = 20)
        nameSMA1   = 'SMA' + str(nSMA1)
        nSMA2      = cols[2].number_input('SMA Long', value = 50)
        nameSMA2   = 'SMA' + str(nSMA2)
        nRSI      = cols[3].number_input('RSI Period', value = 14)
        nameRSI   = 'RSI' + str(nRSI)

        # Retrieve and process data 
        dfPrice = ss.data.history(period=namePeriod)
        dfPrice[nameSMA1] = dfPrice['Close'].rolling(window=nSMA1).mean()
        dfPrice[nameSMA2] = dfPrice['Close'].rolling(window=nSMA2).mean()
        dfPrice[nameRSI]  = calcRSI(dfPrice,window = nRSI)
        dfPrice['LogReturn_pct'] = (np.log(dfPrice['Close']) - np.log(dfPrice['Close'].shift(1)))*100
        dfPrice = dfPrice.reset_index(drop = False)
        dfPrice["Date"] = pd.to_datetime(dfPrice["Date"]).dt.tz_localize(None)

        # Plot
        st.subheader("HISTORICAL PLOT: " + ss.nameTicker)
        fig1 = make_subplots(rows = 3, cols = 1,
                            shared_xaxes = True,
                            vertical_spacing=0.1,
                            row_width=[0.2, 0.05, 0.6],
                            specs=[[{"secondary_y": True}], [{}], [{}]])
        fig1.add_trace(go.Candlestick(
                    x     = dfPrice["Date"],
                    open  = dfPrice['Open'],
                    high  = dfPrice['High'],
                    low   = dfPrice['Low'],
                    close = dfPrice['Close'], 
                    name  = 'Price'), 
                    secondary_y = False)
        fig1.add_trace(go.Bar(x       = dfPrice["Date"], 
                                y       = dfPrice['Volume'], 
                                name    ='Volume', 
                                opacity = 0.5), secondary_y = True)
        fig1.append_trace(go.Scatter(x = dfPrice["Date"], y = dfPrice[nameSMA1] , line=dict(color = primaryColor, width=1), name = nameSMA1), 1, 1)
        fig1.append_trace(go.Scatter(x = dfPrice["Date"], y = dfPrice[nameSMA2] , line=dict(color = colorTurquoise, width=1),  name = nameSMA2), 1, 1)
        fig1.update_xaxes(rangebreaks=[{ 'pattern': 'day of week', 'bounds': [6, 1]}])

        fig1.append_trace(go.Scatter(x = dfPrice["Date"], y = dfPrice[nameRSI] , line=dict(color = primaryColor, width=1),  name = nameRSI), 3, 1)
        fig1.add_shape(dict(type = 'line', x0 = min(dfPrice["Date"]), y0 = 30, x1 = max(dfPrice["Date"]), y1 = 30, line=dict(color = 'grey', width=1, dash = 'dot')), row = 3, col = 1)
        fig1.add_shape(dict(type = 'line', x0 = min(dfPrice["Date"]), y0 = 70, x1 = max(dfPrice["Date"]), y1 = 70, line=dict(color = 'grey', width=1, dash = 'dot')), row = 3, col = 1)

        fig1.update_layout(
            xaxis_rangeslider_visible = True,
            yaxis_title   = 'Price',
            template      = 'plotly_white',
            hovermode     = 'x unified',
            paper_bgcolor = 'rgb(255, 255, 255)',
            plot_bgcolor  = 'rgb(255, 255, 255)',
            
            height        = 600,
            title_text    = ss.nameTicker + ':' + ss.dfDataAnalysis.loc[count,"shortName"]
        )

        fig1.update_yaxes(range=[ min(dfPrice['Volume']) , max(dfPrice['Volume']) * 2], secondary_y = True)
        fig1.layout.yaxis2.showgrid=False

        st.plotly_chart(fig1, use_container_width=True, height = 800)

        # CALENDAR PLOT 
        st.subheader("CALENDER PLOT: " + ss.nameTicker)
        nameParam = st.selectbox("Parameter", ["LogReturn_pct", "Volume"])
        if nameParam == "LogReturn_pct":
            fig1 = calplot(dfPrice, x = "Date", y = "LogReturn_pct", years_title=True, space_between_plots = 0.15, colorscale="RdYlGn", cmap_min = -5, cmap_max = 5)
        else:
            fig1 = calplot(dfPrice, x = "Date", y = "Volume",years_title=True, space_between_plots = 0.15, colorscale = "Greens")

        st.plotly_chart(fig1, use_container_width= True)


    timetrack['plot graph'] = np.round(time.time() - time_start)

    #===================================================================================
    # Financial Statement
    if ss.typeTicker == 'EQUITY':
        with st.expander("Financial Statement:", expanded = True):
            # User Input 1
            cols = st.columns([1,2,2])  
            nameTimeInterval = cols[0].selectbox("Interval", options = ['Annually','Quarterly' ])

            # Process data
            if nameTimeInterval == 'Quarterly':
                listFS      = list(ss.data.quarterly_financials.T.keys())
                dfFinancial = ss.data.quarterly_financials.T
            else:
                listFS      = list(ss.data.financials.T.keys())
                dfFinancial = ss.data.financials.T
                dfFinancial   = calcGrowth(dfFinancial)

            listFS.sort()   
            # st.write(listFS)     

            # User Input 2
            nameFS1 = cols[1].selectbox("Graph 1:", options = listFS, index = listFS.index('Total Revenue'))
            nameFS2 = cols[2].selectbox("Graph 2:", options = listFS, index = listFS.index('Net Income'))
            cols = st.columns([1,2,2])  
            nameFS3 = cols[1].selectbox("Graph 3:", options = listFS, index = listFS.index('Selling General And Administration'))
            nameFS4 = cols[2].selectbox("Graph 4:", options = listFS, index = listFS.index('Cost Of Revenue'))

            # Plot
            fig2 = make_subplots(rows = 2, cols = 2,
                                subplot_titles=(nameFS1, nameFS2, nameFS3, nameFS4),
                                shared_xaxes = True)

            fig2.add_trace(go.Bar( x = dfFinancial.index,
                                y = dfFinancial[nameFS1],
                                text = dfFinancial[nameFS1 + '_Growth(pct)'],
                                name = nameFS1), 1,1)
            fig2.add_trace(go.Bar( x = dfFinancial.index,
                                y = dfFinancial[nameFS2],
                                text = dfFinancial[nameFS2 + '_Growth(pct)'],
                                name = nameFS2), 1,2)
            fig2.add_trace(go.Bar( x = dfFinancial.index,
                                y = dfFinancial[nameFS3],
                                text = dfFinancial[nameFS3 + '_Growth(pct)'],
                                name = nameFS1), 2,1)
            fig2.add_trace(go.Bar( x = dfFinancial.index,
                                y = dfFinancial[nameFS4],
                                text = dfFinancial[nameFS4 + '_Growth(pct)'],
                                name = nameFS2), 2,2)

            fig2.update_traces(marker_color = primaryColor, texttemplate='%{text:.2s}'+ '%')
            fig2.update_layout({'plot_bgcolor': 'rgb(255, 255, 255)',
                                'paper_bgcolor': 'rgb(255, 255, 255)',
                                'showlegend'    : False,
                                'title_text': ss.nameTicker + ':' + ss.dfDataAnalysis.loc[count,"shortName"]
                                })
            st.plotly_chart(fig2, use_container_width=True)
    timetrack['plot statement'] = np.round(time.time() - time_start)

    #===================================================================================
    with st.expander("Information:"):
        try:
            st.caption(ss.dfDataAnalysis.loc[count,"longBusinessSummary"])
            col1, col2 = st.columns(2)
            
            col1.write("Sector: " + ss.dfDataAnalysis.loc[count,"sector"])
            col2.write("Industry: " + ss.dfDataAnalysis.loc[count,"industry"])
        except:
            pass

        try:
            st.caption(ss.dfDataAnalysis.loc[count,"description"])
        except:
            pass
    #===================================================================================
    with st.expander("Recommendation:"):
        try:
            df = ss.data.recommendations.sort_index(ascending=False)
            df.index = df.index.strftime('%d/%m/%Y')
            st.dataframe(df)
        except:
            pass

    #===================================================================================
    with st.expander("Holder:"):
        try:
            
            df = ss.data.institutional_holders
            df['Date Reported'] = df['Date Reported'].dt.strftime('%d/%m/%Y')

            df['Value_(B)'] = df['Value']/1e9
            df['Shares_(M)'] = df['Shares']/1e6
            df = df.drop(['Value'], axis = 1)      
            df = df.drop(['Shares'], axis = 1)
            st.dataframe(df)
            
        except:
            pass

    timetrack['load info'] = np.round(time.time() - time_start)
      
    #===================================================================================
    with st.expander("Options:", expanded = True):
      
        
        #
        def calcOption(S, X, sig, r, q, datePricing, dateExpiry):
            t = (dateExpiry - datePricing).day/365
            
            N1 = log(S/X)
            N2 = t * ( r - q + (sig**2)/2)
            D1 = sig * sqrt(t)
            d1 = (N1 + N2)/D1
            d2 = d1 - D1 

            Npd1 = norm.cdf(d1)
            Nnd1 = norm.cdf(-d1)
            Npd2 = norm.cdf(d2)
            Nnd2 = norm.cdf(-d2)

            eqt = exp(-q*t)
            ert = exp(-r*t)

            # Greeks
            delta_call = eqt * Npd1
            delta_put  = ert * (Npd1 - 1)

            theta_call = (- (S * exp(-1 * (d1**2)/2) / sqrt(2*pi) * sig * eqt/ (2*sqrt(t))) - (r * X * ert * Npd2) + (q * S * eqt * Npd1))/365
            theta_put  = (- (S * exp(-1 * (d1**2)/2) / sqrt(2*pi) * sig * eqt/ (2*sqrt(t))) + (r * X * ert * Nnd2) - (q * S * eqt * Nnd1))/365

            gamma = exp(-1*(d1**2)/2) / sqrt(2*pi) * eqt / (S*D1)
            vega  = exp(-1*(d1**2)/2) / sqrt(2*pi) * eqt * S * sqrt(t)/100
            
            rho_call = X*t*ert*Npd2/100
            rho_put  = -X*t*ert*Nnd2/100

            price_call = S*Npd1*eqt - X*ert*Npd2 
            price_put  = X*ert*Nnd2 - S*eqt*Nnd1

            dfResult = pd.DataFrame.from_dict({
                "UNDERLYING"    : [S],
                "STRIKE"        : [X],
                "VOLATILITY"    : [sig],
                "INTEREST_RATE" : [r],
                "DIVIDEND_RATE" : [q],
                "START"         : [datePricing],
                "EXPIRY"        : [dateExpiry],
                "CALL_PRICE"    : [price_call],
                "PUT_PRICE"     : [price_put],
                "CALL_DELTA"    : [delta_call],
                "PUT_DELTA"     : [delta_put],
                "CALL_RHO"      : [rho_call],
                "PUT_RHO"       : [rho_put],
                "CALL_THETA"    : [theta_call],
                "PUT_THETA"     : [theta_put],
                "GAMMA"         : [gamma],
                "VEGA"          : [vega],
            })
            return dfResult

        try:
            # User Input
            boolFirstRunOption = False
            if not boolFirstRunOption:
                ss.dateOption = ss.data.options[0]
            idxOption     = ss.data.options.index(ss.dateOption)

            ss.dateOption = st.selectbox("Expiration Date", options = ss.data.options, index = idxOption)
            dfOptionCall  = ss.data.option_chain(ss.dateOption).calls
            dfOptionPut   = ss.data.option_chain(ss.dateOption).puts

            # Plot 
            figOption = make_subplots(rows =3 , cols = 2, shared_xaxes = True)
            figOption.append_trace(go.Scatter(x = dfOptionCall['strike'], y = dfOptionCall['lastPrice'] , 
                                            legendgroup = 'Call', showlegend = False,
                                            mode = 'lines' ,line=dict(color = colorTurquoise, width=1), name = 'Call'), 1, 1)
            
            figOption.append_trace(go.Scatter(x = dfOptionPut['strike'], y = dfOptionPut['lastPrice'] , 
                                            legendgroup = 'Put', showlegend = False,
                                            mode = 'lines', line=dict(color = primaryColor, width=1), name = 'Put'), 1, 1)
            # figOption.update_xaxes(title_text= 'Strike Price', row=1, col=1)
            figOption.update_yaxes(title_text= 'Price', row=1, col=1)
            figOption.add_shape(dict(type = 'line', x0 = ss.currentPrice, y0 = np.min(dfOptionPut['lastPrice']), x1 = ss.currentPrice, y1 = np.max(dfOptionPut['lastPrice']), line=dict(color = 'grey', width=1, dash = 'dot')), row = 1, col = 1)


            figOption.append_trace(go.Scatter(x = dfOptionCall['strike'], y = dfOptionCall['openInterest'] , 
                                            legendgroup = 'Call', showlegend = False,
                                            mode = 'lines' ,line=dict(color = colorTurquoise, width=1), name = 'Call'), 1, 2)
            
            figOption.append_trace(go.Scatter(x = dfOptionPut['strike'], y = dfOptionPut['openInterest'] , 
                                            legendgroup = 'Put', showlegend = False,
                                            mode = 'lines', line=dict(color = primaryColor, width=1), name = 'Put'), 1, 2)
            # figOption.update_xaxes(title_text= 'Strike Price', row=1, col=2)
            figOption.update_yaxes(title_text= 'Open Interest', row=1, col=2)
            figOption.add_shape(dict(type = 'line', x0 = ss.currentPrice, y0 = np.min(dfOptionPut['openInterest']), x1 = ss.currentPrice, y1 = np.max(dfOptionPut['openInterest']), line=dict(color = 'grey', width=1, dash = 'dot')), row = 1, col = 2)

            figOption.append_trace(go.Scatter(x = dfOptionCall['strike'], y = dfOptionCall['impliedVolatility'] , 
                                            legendgroup = 'Call', showlegend = False,
                                            mode = 'lines' ,line=dict(color = colorTurquoise, width=1), name = 'Call'), 2, 1)
            
            figOption.append_trace(go.Scatter(x = dfOptionPut['strike'], y = dfOptionPut['impliedVolatility'] , 
                                            legendgroup = 'Put', showlegend = False,
                                            mode = 'lines', line=dict(color = primaryColor, width=1), name = 'Put'), 2, 1)
            # figOption.update_xaxes(title_text= 'Strike Price', row=2, col=1)
            figOption.update_yaxes(title_text= 'Implied Volatility', row=2, col=1)
            figOption.add_shape(dict(type = 'line', x0 = ss.currentPrice, y0 = np.min(dfOptionPut['impliedVolatility']), x1 = ss.currentPrice, y1 = np.max(dfOptionPut['impliedVolatility']), line=dict(color = 'grey', width=1, dash = 'dot')), row = 2, col = 1)

            figOption.append_trace(go.Scatter(x = dfOptionCall['strike'], y = dfOptionCall['volume'] , 
                                            legendgroup = 'Call', showlegend = False,
                                            mode = 'lines' ,line=dict(color = colorTurquoise, width=1), name = 'Call'), 2, 2)
            
            figOption.append_trace(go.Scatter(x = dfOptionPut['strike'], y = dfOptionPut['volume'] , 
                                            legendgroup = 'Put', showlegend = False,
                                            mode = 'lines', line=dict(color = primaryColor, width=1), name = 'Put'), 2, 2)
            # figOption.update_xaxes(title_text= 'Strike Price', row=2, col=2)
            figOption.update_yaxes(title_text= 'Volume', row=2, col=2)
            figOption.add_shape(dict(type = 'line', x0 = ss.currentPrice, y0 = np.min(dfOptionPut['volume']), x1 = ss.currentPrice, y1 = np.max(dfOptionPut['volume']), line=dict(color = 'grey', width=1, dash = 'dot')), row = 2, col = 2)

            figOption.append_trace(go.Scatter(x = dfOptionCall['strike'], y = dfOptionCall['strike']/dfOptionCall['lastPrice'] , 
                                            legendgroup = 'Call', showlegend = False,
                                            mode = 'lines' ,line=dict(color = colorTurquoise, width=1), name = 'Call'), 3, 1)
            
            figOption.append_trace(go.Scatter(x = dfOptionPut['strike'], y = dfOptionPut['strike']/dfOptionPut['lastPrice'] , 
                                            legendgroup = 'Put', showlegend = False,
                                            mode = 'lines', line=dict(color = primaryColor, width=1), name = 'Put'), 3, 1)
            figOption.update_xaxes(title_text= 'Strike Price', row=3, col=1)
            figOption.update_yaxes(title_text= 'Strike/Price', row=3, col=1)
            figOption.add_shape(dict(type = 'line', x0 = ss.currentPrice, y0 = np.min(dfOptionPut['strike']/dfOptionPut['lastPrice']), x1 = ss.currentPrice, y1 = np.max(dfOptionPut['strike']/dfOptionPut['lastPrice']), line=dict(color = 'grey', width=1, dash = 'dot')), row = 3, col = 1)

            figOption.append_trace(go.Scatter(x = dfOptionCall['strike'], y = dfOptionCall['percentChange']/ss.pctChangePrice, 
                                            legendgroup = 'Call', showlegend = False,
                                            mode = 'lines' ,line=dict(color = colorTurquoise, width=1), name = 'Call'), 3, 2)
            
            figOption.append_trace(go.Scatter(x = dfOptionPut['strike'], y = dfOptionPut['percentChange']/ss.pctChangePrice, 
                                            legendgroup = 'Put', showlegend = False,
                                            mode = 'lines', line=dict(color = primaryColor, width=1), name = 'Put'), 3, 2)
            figOption.update_xaxes(title_text= 'Strike Price', row=3, col=2)
            figOption.update_yaxes(title_text= 'Option to price change', row=3, col=2)
            figOption.add_shape(dict(type = 'line', x0 = ss.currentPrice, y0 = np.min(dfOptionPut['percentChange']/ss.pctChangePrice), x1 = ss.currentPrice, y1 = np.max(dfOptionPut['percentChange']/ss.pctChangePrice), line=dict(color = 'grey', width=1, dash = 'dot')), row = 3, col = 2)
            # figOption.add_shape(dict(type = 'line', x0 = ss.currentPrice, y0 = -np.inf, x1 = ss.currentPrice, y1 = np.inf, line=dict(color = 'grey', width=1, dash = 'dot')), row = 3, col = 2)

            figOption.update_layout({'plot_bgcolor'   : 'rgb(255, 255, 255)',
                                'paper_bgcolor'       : 'rgb(255, 255, 255)',
                                'showlegend'          : True,
                                'legend_title_text'   : 'Contract Type',
                                'legend_itemclick'    : 'toggleothers',
                                'hovermode'           : 'x unified',
                                'legend'              : dict(y =1.1, orientation="h"),
                                'title_text': ss.nameTicker + ':' + ss.dfDataAnalysis.loc[count,"shortName"] + " / Option Expiration: " + ss.dateOption ,
                                })

            st.plotly_chart(figOption, use_container_width=True)

        except:
            pass

    timetrack['load option'] = np.round(time.time() - time_start)

  # st.write(timetrack)

# =============================================================================================================

