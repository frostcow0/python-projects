# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:43:50 2021

@author: gamet
"""

# I need to separate all of these functions to improve overall speed.

import re
import json
import csv
from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup # Had to Conda install this.
import requests

def pull(stock):
    url_stats='https://finance.yahoo.com/quote/{}/key-statistics?p={}' # To do
    url_profile='https://finance.yahoo.com/quote/{}/profile?p={}' # To Do
    
    annual_cf=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
    quarterly_cf=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']
    
    annual_bs=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
    quarterly_bs=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']

    #-----------------------#

    #annual_is[0]['operatingIncome'] outputs = {'raw': -8975000000, 'fmt': '-8.97B', 'longFmt': '-8,975,000,000'}
    
    # Consolidate annual income sheet
    annual_is_stmts=[]
    for s in annual_is:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        annual_is_stmts.append(statement)
        
    # Quarterly, too
    quarterly_is_stmts=[]
    for s in quarterly_is:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        quarterly_is_stmts.append(statement)
        
    # Consolidate annual cash flows
    annual_cf_stmts=[]
    for s in annual_cf:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        annual_cf_stmts.append(statement)
        
    # Quarterly, too
    quarterly_cf_stmts=[]
    for s in quarterly_cf:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        quarterly_cf_stmts.append(statement)
        
    # Consolidate annual balance sheet
    annual_bs_stmts=[]
    for s in annual_bs:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        annual_bs_stmts.append(statement)
        
    # Quarterly, too
    quarterly_bs_stmts=[]
    for s in quarterly_bs:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        quarterly_bs_stmts.append(statement)
        
    #-----------------------#
    
    # Getting the Profile data
    response=requests.get(url_profile.format(stock,stock)) # These all do the same stuff as above.
    soup=BeautifulSoup(response.text,'html.parser')
    pattern=re.compile(r'\s--\sData\s--\s') 
    script_data=soup.find('script',text=pattern).contents[0]
    start=script_data.find('context')-2
    json_data=json.loads(script_data[start:-12])
    
# =============================================================================
#     json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['companyOfficers']
#     json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['longBusinessSummary']
#     json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['secFilings']['filings']
# =============================================================================
    
    json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail'] # Interesting stuff to look at
    
    #-----------------------#
    
    # Getting the Statistics data
    response=requests.get(url_stats.format(stock,stock)) # These all do the same stuff as above.
    soup=BeautifulSoup(response.text,'html.parser')
    pattern=re.compile(r'\s--\sData\s--\s') 
    script_data=soup.find('script',text=pattern).contents[0]
    start=script_data.find('context')-2
    json_data=json.loads(script_data[start:-12])
    
    json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics'] # More cool info
    
    #-----------------------#
    
def pull_financials(stock):    
    url_financials='https://finance.yahoo.com/quote/{}/financials?p={}'
    
    response=requests.get(url_financials.format(stock,stock)) # Pulls the page.

    soup=BeautifulSoup(response.text,'html.parser') # Parses the page.

    pattern=re.compile(r'\s--\sData\s--\s') # The point in the page's source code where the data-obtaining javascripts are.
    script_data=soup.find('script',text=pattern).contents[0]

    start=script_data.find('context')-2 # We want to start two characters after the word context to avoid the javascript.

    json_data=json.loads(script_data[start:-12]) # We don't want the last 12 characters in the string. JSON loads returns a Dictionary.

    annual_is=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
    quarterly_is=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']
    
    annual_cf=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
    quarterly_cf=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']
    
    annual_bs=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
    quarterly_bs=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']
    
      # Consolidate annual income sheet
    annual_is_stmts=[]
    for s in annual_is:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        annual_is_stmts.append(statement)
        
    # Quarterly, too
    quarterly_is_stmts=[]
    for s in quarterly_is:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        quarterly_is_stmts.append(statement)
        
    # Consolidate annual cash flows
    annual_cf_stmts=[]
    for s in annual_cf:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        annual_cf_stmts.append(statement)
        
    # Quarterly, too
    quarterly_cf_stmts=[]
    for s in quarterly_cf:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        quarterly_cf_stmts.append(statement)
        
    # Consolidate annual balance sheet
    annual_bs_stmts=[]
    for s in annual_bs:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        annual_bs_stmts.append(statement)
        
    # Quarterly, too
    quarterly_bs_stmts=[]
    for s in quarterly_bs:
        statement={}
        for key, val in s.items(): # Pulls the row and its important columns
            try: # Not all keys have a val.
                statement[key]=val['raw']
            except TypeError:
                continue
            except KeyError:
                continue
        quarterly_bs_stmts.append(statement)
    
    return {'annual is':pd.DataFrame(annual_is).T,
            'quarterly is':pd.DataFrame(quarterly_is).T,
            'annual cf':pd.DataFrame(annual_cf).T,
            'quarterly cf':pd.DataFrame(quarterly_cf).T,
            'annual bs':pd.DataFrame(annual_bs).T,
            'quarterly bs':pd.DataFrame(quarterly_bs).T,
            'annual is stmts':pd.DataFrame(annual_is_stmts).T}
def pull_historical(stock):
    # Getting the Historical data
    stock_url='https://query1.finance.yahoo.com/v7/finance/download/{}?'
    
    params={
            'range':'7d',
            'interval':'1d',
            'events':'history'
        }
    
    response=requests.get(stock_url.format(stock),params=params)
    
    file=StringIO(response.text)
    reader=csv.reader(file)
    data=list(reader)
    frame=pd.DataFrame()
    for row in data[:8]:
        temp=pd.Series(row,name='stock')
        frame=pd.concat([frame,temp],axis=1) # I'm pretty sure concat is slower.
    frame=frame.T # Rotates the frame 90 degrees.
    
    return frame

def pull_current(stock):
    stock_url='https://query1.finance.yahoo.com/v8/finance/chart/{}?'
    
    params={
        'region':'US',
        'range':'1d',
        'interval':'5m',
        'includeTimestamps':'false'
        }
    response=requests.get(stock_url.format(stock),params=params) # 200 Response.
    
    file=StringIO(response.text)
    reader=csv.reader(file)
    data=list(reader)
    d={
       data[0][9][:18]:data[0][9][19:],
       data[0][11][:13]:data[0][11][14:]
       }
    
    #df=pd.Series(data=d)
    
    #frame=pd.DataFrame()
    #for row in data[:8]:
    #    temp=pd.Series(row)
    #    frame=pd.concat([frame,temp],axis=1)
    #frame=frame.T # Rotates the frame 90 degrees.
    
    return d

def pull_trending(count): # Count is how many we pull. Yahoo's default is 5.
    url='https://query1.finance.yahoo.com/v1/finance/trending/US?count={}'
    response=requests.get(url.format(count))
    