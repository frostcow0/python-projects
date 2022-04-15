# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:33:42 2021

@author: gamet
"""
from stock_frame_pull import *
import matplotlib.pyplot as plt
import time
import os

clear=lambda:os.system('cls')

tickers=input('What tickers would you like to watch? : ').upper().split(' ')

def keyword_check(tickers):
    placeholder_airlines=['UAL','AAL','DAL','SAVE']
    if 'AIRLINES' in tickers:
        tickers.pop(tickers.index('AIRLINES'))
        for ticker in placeholder_airlines:
            tickers.append(ticker)
    return tickers

def plot_old(frame):
    df=frame
    plt.plot(frame[0],frame[4])

def get_ticker(tickers): # 200 response, no frame.
    current={}
    for i in tickers:
        current[i]=pull_current(i)
        #print('~'*3,i,'- current pulled.')
    return current
        
def get_historical(tickers):
    frames={}
    for i in tickers:
        frames[i]=pull_historical(i)
    return frames

def get_financials(ticker):
    sheets={}
    for i in tickers:
        sheets[i]=pull_financials(i)
    return sheets

def current_frame(ticker):
    temp={}
    for i in tickers:
        temp[i]=ticker['current'][i]
    return pd.DataFrame(data=temp,columns=tickers)
    
def find_difference(current):
    for i in current: #current[i][0] is prev close, 1 is price
        diff=round(float(current[i][1])-float(current[i][0]),2)
        if diff<0:
            word='UP'
        elif diff==0:
            print(i,'is currently equal to yesterday\'s close.')
        else:
            word='DOWN'
        print(i,'is',word,'by   $',abs(diff),'\n')
    print('-'*21,' Done ','-'*21,'\n')
    
    return True # for fun

def chart(current):
    done=False
    while done!=True:
        time.sleep(30)
        temp={}
        tick=get_ticker(tickers)
        for i in current:
            temp[i]=tick[i]['regularMarketPrice']
        clear()
        current=current.append(temp,ignore_index=True)
        print(current.iloc[::-1].head(5),'\n\n')
        
    print('*'*30,'Stopping.')    
    
def init(ticker):
    ticker=keyword_check(ticker)
    ticker={
        'history':get_historical(tickers),
        'current':get_ticker(tickers),
        'financial':get_financials(tickers)
        }
    print('-'*20,' Loaded ','-'*20,'\n')
    
    current=current_frame(ticker)
    print(current,'\n')
    find_difference(current)
    
    chart(current)
    
    return ticker

total=init(tickers)


# To use a Dict or a Frame, that is the question.

# Maybe the sheets are one layer too deep? Or index them.
# The annual statements need to be sum of the columns.

# Need to fix the clearing part