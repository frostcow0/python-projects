# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:33:42 2021

@author: gamet
"""
from stock_frame_pull import *
import matplotlib.pyplot as plt

tickers=input('What tickers would you like to watch? : ').upper().split(' ')

def plot_old(frame):
    df=frame
    plt.plot(frame[0],frame[4])

def get_ticker(tickers): # 200 response, no frame.
    current={}
    for i in tickers:
        current[i]=pull_current(i)
        print('~'*3,i,'- current pulled.')
    return current
        
def get_historical(tickers):
    frames={}
    for i in tickers:
        frames[i]=pull_historical(i)
        print('~'*3,i,'- history pulled.')
        #plot_old(frames[i+' History'])
    return frames

def get_financials(ticker):
    sheets={}
    for i in tickers:
        sheets[i]=pull_financials(i)
        print('~'*3,i,'- financial pulled.')
    return sheets

def init(tickers):
    history=get_historical(tickers) # Close of today's is Current Price.
    current=get_ticker(tickers) # regularMarketPrice & previousClose
    financial=get_financials(tickers)
        
    return history,current,financial

test=init(tickers)

# To use a Dict or a Frame, that is the question.

# Maybe the sheets are one layer too deep? Or index them.