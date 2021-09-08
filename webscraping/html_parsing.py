import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# url     = 'https://en.wikipedia.org/wiki/Chinampa'
url     = 'https://en.wikipedia.org/wiki/Long_Walls'
text    = requests.get(url).text
soup    = BeautifulSoup(text, 'html.parser')

def parsinTime(reflist):
    data = {
        'Author': [],
        'The rest :)': []
    }
    for ref in reflist.find_all('li'): # Each reference
        reference = re.sub(r'^[\^\sa-z]+', '', ref.text)
        reference = reference.replace('.\n', '')
        splitRef = reference.split('. ')
        data['Author'].append(splitRef[0])
        try:
            data['The rest :)'].append(splitRef[1])
        except:
            data['The rest :)'].append('')
    df = pd.DataFrame(data)
    print(df)

if __name__ == '__main__':
    content = soup.find(id = 'content')
    if content:
        bodyContent = content.find(id = 'bodyContent')
        if bodyContent:
            contentText = bodyContent.find(id = 'mw-content-text')
            if contentText:
                reflist = contentText.find('div', {'class': 'reflist reflist-columns references-column-width reflist-columns-2'})
                if reflist:
                    parsinTime(reflist)
                else:
                    parser = contentText.find(id = 'mw-parser-output')
                    if parser:
                        reflist = contentText.find('div', {'class': 'reflist'})
                        if reflist:
                            parsinTime(reflist)
                        else:
                            print("No reflist")
                    else:
                        print("No reflist or parser")
            else:
                print("No contentText")
        else:
            print("No bodyContent")
    else:
        print("No content")
