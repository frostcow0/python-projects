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
        print('~'*3,i,'- current pulled.')
        current[i]=pull_current(i)
    return current
        
def get_historical(tickers):
    frames={}
    for i in tickers:
        frames[i]=pull_historical(i)
        print('~'*3,i,'- history pulled.')
        #plot_old(frames[i+' History'])
    return frames

def init(tickers):
    history=get_historical(tickers) # Close of today's is Current Price.
    current=get_ticker(tickers) # regularMarketPrice & previousClose
        
    return currentPrices

current=get_ticker(tickers)
test= init(tickers)

# Printing the rows to try and figure out how to get the data that I need
# from the current info. looks like i want rows 9 & 10, now I just need to 
# pull those, put the leading text as column headers, and throw it into a frame.