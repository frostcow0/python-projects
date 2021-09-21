import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url     = 'https://en.wikipedia.org/wiki/Chinampa'
text    = requests.get(url).text
soup    = BeautifulSoup(text, 'html.parser')

content = soup.find()