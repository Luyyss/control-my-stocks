import psycopg2

class database:
    
    def __init__(self, data):
        self.__data = data

    def connect(self):
        self.__conn = conn = psycopg2.connect(
            database=self.__data['name'], user=self.__data['user'], password=self.__data['passw'], host=self.__data['host'], port= '5432'
        )

    def createTables(self):

        cursor = self.__conn.cursor()

        #tb_stock ( id, code, name, total_qtd, avg_cost, last_price )
        cursor.execute("DROP TABLE IF EXISTS tb_stock")

        sql ='''CREATE TABLE tb_stock(
            code CHAR(5) NOT NULL,
            name CHAR(200),
            total_qtd INT,
            avg_cost FLOAT,
            last_price FLOAT
        )'''

        cursor.execute(sql)
        
        # tb_lot ( id, stock_id, qtd, cost, dt_buy )
        cursor.execute("DROP TABLE IF EXISTS tb_lot")

        sql ='''CREATE TABLE tb_lot(
            code CHAR(5) NOT NULL,
            qtd int,
            cost FLOAT,
            dt_buy CHAR(10)
        )'''

        cursor.execute(sql)
        
        #tb_summary ( amount_cost, stock_price_sum )
        cursor.execute("DROP TABLE IF EXISTS tb_summary")

        sql ='''CREATE TABLE tb_summary(
            amount_cost FLOAT,
            stock_price_sum FLOAT
        )'''

        cursor.execute(sql)

        print("Tables created successfully........")

        self.__conn.close()