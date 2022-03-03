from time import sleep
from selenium import webdriver


URL = 'https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html'

def initialize(url) -> webdriver.Firefox:
    """Uses selenium-gecko driver to open webpage"""
    driver = webdriver.Firefox()
    driver.get(url)
    return driver

def main():
    driver = initialize(URL)
    sleep(4)


if __name__ == '__main__':
    main()
