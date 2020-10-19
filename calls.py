from src.classes.DataBase import DataBase
from src.utils.defaults import variables as va
import src.utils.functions as funcs
from src.classes.StockControll import StockControll
from flask import jsonify

import numpy as np

db = DataBase(va['DATABASE'])
db.createTables()

db.insert('tb_stock', ['code', 'name'], ['BBSE3', 'BB Seguridade']) #, '0', '0', '0'
db.insert('tb_stock', ['code', 'name'], ['ITSA4', 'Itaúsa']) #, 'total_qtd', 'avg_cost', 'last_price'

all_stocks = db.select('tb_stock', ['code', 'total_qtd'])
print(all_stocks)

# for stock, amount in all_stocks:
#     print(stock, amount)
# db.close()

# a = ['code', 'name', 'total_qtd', 'avg_cost', 'last_price']

# print( funcs.joinDict(a) )

# from lxml import html

# funcs.getAllStocksSymbols()
# d = {k:v for k in range(3)}
# v = '%'
# d = np.full((1,3), v)
# print(d)
# print(funcs.joinDict(d[0]))

# print(funcs.getAllStocksSymbols())

# print( jsonify( funcs.readStocksFile() ) )

# a = {'code':'ITSA4', 'size':'35'}
# r = ''
# for key, elem in a.items():
#     r += key + " = '"+ elem + "', "

# print( r[0:-2] )

# stc = StockControll()
# stock = 'BRAP4'
# stc.removeStock(stock, db)

# all_stocks = db.select('tb_stock', ['code', 'name', 'total_qtd'])
# print(all_stocks)

# stc = StockControll()
# stc.addLot('ITSA4', '2020-10-19', '15', '9.37', db)

# all_lots = db.select('tb_lot')
# print(all_lots)