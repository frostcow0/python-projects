# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 11:37:11 2021

@author: gamet
"""
beg=float(input('Beginning Value of Investment: '))
end=float(input('Ending Value of Investment: '))
weeks=float(input('Number of Weeks: '))

aror=((end/beg)**(1/(weeks/52)))-1
aror*=100

print('')
print('The annualized rate of return is {:.2f} percent.'.format(aror))

#beg is 2357.63
#end is 2424.61
#weeks is 13
#ans is 11.9%