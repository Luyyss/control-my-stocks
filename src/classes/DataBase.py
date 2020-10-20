import psycopg2
import numpy as np
import src.utils.functions as funcs

class DataBase:

    def __init__(self, data):
        self.__data = data
        self.__conn = conn = psycopg2.connect(
            database=self.__data['name'], user=self.__data['user'], password=self.__data['passw'], host=self.__data['host'], port= '5432'
        )

    def insert(self, table, cols, args):

        vals = np.full((1,len(args)), '%s')[0]

        sql = 'INSERT INTO '+table+' ('+funcs.joinDict(cols)+') VALUES ('+funcs.joinDict(vals)+')'

        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(sql, args)
        self.__conn.commit()

    def delete(self, table, where=None, adicional=None):

        sql = 'DELETE FROM '+table

        if where != None:
            aux = ''
            for key, elem in where.items():
                aux += key + " = '"+ elem + "', "

            sql += ' WHERE '+ aux[0:-2]

        if adicional != None:
            sql += adicional

        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(sql)
        self.__conn.commit()


    def update(self, table, data, where=None, adicional=None):

        sql = 'UPDATE '+table

        aux = ''
        for key, elem in data.items():
            aux += key + " = '"+ elem + "', "

        sql += ' SET '+ aux[0:-2]

        if where != None:
            aux = ''
            for key, elem in where.items():
                aux += key + " = '"+ elem + "', "

            sql += ' WHERE '+ aux[0:-2]

        if adicional != None:
            sql += adicional

        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(sql)
        self.__conn.commit()


    def select(self, table, cols=None, where=None, adicional=None):

        cols = '*' if cols == None else funcs.joinDict(cols)

        sql = 'SELECT '+cols+' FROM '+ table

        if where != None:
            aux = ''
            for key, elem in where.items():
                aux += key + " = '"+ elem + "', "

            sql += ' WHERE '+ aux[0:-2]

        if adicional != None:
            sql += adicional

        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(sql)

        rows = self.__cursor.fetchall()

        return rows

    def close(self):
        if hasattr(self, '__cursor'):
            self.__cursor.close()
        self.__conn.close()

    def createTables(self):

        self.__cursor = self.__conn.cursor()

        #tb_stock ( id, code, name, total_qtd, avg_cost, last_price )
        self.__cursor.execute("DROP TABLE IF EXISTS tb_stock")

        sql ='''CREATE TABLE tb_stock(
            code CHAR(5) UNIQUE NOT NULL,
            name CHAR(200),
            total_qtd INT DEFAULT 0,
            avg_cost FLOAT DEFAULT 0
        )'''

        # last_price FLOAT DEFAULT 0

        self.__cursor.execute(sql)
        
        # tb_lot ( id, stock_id, qtd, cost, dt_buy )
        self.__cursor.execute("DROP TABLE IF EXISTS tb_lot")

        sql ='''CREATE TABLE tb_lot(
            id SERIAL PRIMARY KEY,
            code CHAR(5) NOT NULL,
            qtd int,
            cost FLOAT,
            dt_buy CHAR(10)
        )'''

        self.__cursor.execute(sql)
        
        #tb_summary ( amount_cost, stock_price_sum )
        self.__cursor.execute("DROP TABLE IF EXISTS tb_summary")

        sql ='''CREATE TABLE tb_summary(
            amount_cost FLOAT,
            stock_price_sum FLOAT
        )'''

        self.__cursor.execute(sql)
        self.__conn.commit()