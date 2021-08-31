import requests
from bs4 import BeautifulSoup

url     = 'https://en.wikipedia.org/wiki/Chinampa'
text    = requests.get(url).text
soup    = BeautifulSoup(text, 'html.parser')

# print(soup.get_text())

if __name__ == '__main__':
    content = soup.find(id = 'content')
    if content:
        bodyContent = content.find(id = 'bodyContent')
        if bodyContent:
            contentText = bodyContent.find(id = 'mw-content-text')
            if contentText:
                reflist = contentText.find('div', {'class': 'reflist reflist-columns references-column-width reflist-columns-2'})
                if reflist:
                    for ref in reflist.find_all('li'):
                        print(ref)
                        print('-'*40)

                else:
                    print("No reflist")
            else:
                print("No contentText")
        else:
            print("No bodyContent")
    else:
        print("No content")