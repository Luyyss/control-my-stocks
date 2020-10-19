from src.utils.database import database
from src.utils.defaults import variables as va
import src.utils.functions as funcs

import numpy as np

# db = database(va['DATABASE'])
# db.createTables()

# db.insert('tb_stock', ['code', 'name'], ['BBSE3', 'BB Seguridade']) #, '0', '0', '0'
# db.insert('tb_stock', ['code', 'name'], ['ITSA4', 'Itaúsa']) #, 'total_qtd', 'avg_cost', 'last_price'

# d = db.select('tb_stock')
# print(d)

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

print(funcs.getAllStocksSymbols())