import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url     = 'https://www.classcentral.com/collection/ivy-league-moocs?subject=data-science'
text    = requests.get(url).text
soup    = BeautifulSoup(text, 'html.parser')

def main(args=None):
    found = findContent()
    # print(type(found))
    output = doingSomething(found)
    # print(output)

def findContent():
    content = soup.find(id = 'page-collection')
    if content:
        page = content.select_one('div[class*="contain-page"]')
        if page:
            widthPage = page.select('div[class*="width-page"]')
            if widthPage:
                for width in widthPage:
                    results = width.select_one('div[class*="results"]')
                    if results:
                        result = results.select_one('ol[class*="course-list"]')
                        if result:
                            each = result.select('li')
                            if each:
                                return each
                            else:
                                print('no each')
                        else:
                            print('no result')
                    else:
                        print('no results')

def doingSomething(found):
    for course in found:
        print('='*60)
        print(course.title)

if __name__ == '__main__':
    main()