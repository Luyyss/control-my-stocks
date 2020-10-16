from lxml import html
from lxml import etree
from urllib.request import urlopen
from src.utils.defaults import variables as va

def getWebPage(url):
    with urlopen(url) as response:
        return response.read().decode('utf-8')

def getXPathContent(text, xp):
    tree = html.fromstring(text)
    return tree.xpath(xp)[0].text

def getStockUrl(name):
    return va['SCRAPING']['base'] + str(name) + va['SCRAPING']['tag']

def getStockPage(name):
    return getWebPage( getStockUrl( name ) )

def getStockName(page):
    return getXPathContent( page, va['SCRAPING']['xp_name'] )

def getStockPrice(page):
    return getXPathContent( page, va['SCRAPING']['xp_price'] )

def getStockChange(page):
    return getXPathContent( page, va['SCRAPING']['xp_change'] )

def getStockInfo(name):
    page = getStockPage(name)

    data = {
        'name':getStockName(page),
        'price':getStockPrice(page),
        'change':getStockChange(page)
    }

    return data