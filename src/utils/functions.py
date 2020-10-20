from lxml import html, etree
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
        # 'name':getStockName(page),
        'price':getStockPrice(page),
        'change':getStockChange(page)
    }

    return data

def getAllStocksSymbols():

    stocks = []

    page = getWebPage('https://www.infomoney.com.br/cotacoes/empresas-b3/')
    tree = html.fromstring(page)
    content = tree.xpath("//div[contains(@class, 'article-content')]")[0]

    for tbody in content.xpath("//tbody"):
        for tr in tbody:

            name = tr.getchildren()[0].text

            for link in tr.iterlinks():
                code = link[0].text
                if not code.endswith('F') and not code.endswith('34') and not code.endswith('11') and not code.endswith('12'):
                    stocks.append( code + ' | ' + name )

    writeStocksToFile(str(stocks))

    return stocks

def joinDict(d, s=","):
    return str(s.join(d))

def writeStocksToFile(data):
    f = open('stocks.json', 'w')
    f.write(data)
    f.close()

def readStocksFile():

    import ast

    f = open('stocks.json', 'r')
    t = f.read()
    f.close()

    return ast.literal_eval(t)

# def formatFloat(f, d):
#     return f'{"{:."+str(d)+"f}".format(f)}'
        #  f'{"{:.2f}".format(f)}'

# import os
# import platform
# from datetime import date, datetime

# def isModificatedToday(path_to_file):
#     aux = 0
#     if platform.system() == 'Windows':
#         aux = os.path.getmtime(path_to_file)
#     else:
#         stat = os.stat(path_to_file)
#         aux = stat.st_mtime

#     print(date.today().strftime("%d/%m/%Y"))
#     print(datetime.strptime(str(formatFloat(aux, 0)), "%d/%m/%Y"))

#     return date.today().strftime("%d/%m/%Y") == datetime.strptime(aux, "%d/%m/%Y")