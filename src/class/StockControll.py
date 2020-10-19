
class StockControll:

    def addStock(self, code, name, db):
        # db.insert('tb_stock', ['code', 'name'], ['BBSE3', 'BB Seguridade']) #, '0', '0', '0'
        # db.insert('tb_stock', ['code', 'name'], ['ITSA4', 'Itaúsa']) #, 'total_qtd', 'avg_cost', 'last_price'
        db.insert('tb_stock', ['code', 'name'], [code, name])
        return True
        # d = db.select('tb_stock')