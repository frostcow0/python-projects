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

def get_ticker(tickers): # Doesn't pull right. 400 response
    current={}
    for i in tickers:
        current[i+' Current']=pull_current(i)
    return current
        
def get_historical(tickers):
    frames={}
    for i in tickers:
        frames[i+' History']=pull_historical(i)
        print('~'*3,i,'was pulled.')
        plot_old(frames[i+' History'])
    return frames

print(get_ticker(tickers))
print(get_historical(tickers))