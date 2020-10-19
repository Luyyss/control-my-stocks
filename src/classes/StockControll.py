
class StockControll:

    def addStock(self, code, name, db):
        db.insert('tb_stock', ['code', 'name'], [code, name])
        return True

    def removeStock(self, code, db):
        db.delete('tb_stock', {'code':code})
        db.delete('tb_lot', {'code':code})
        return True

    def updateTotal(self, code, qtd, db):
        db.update('tb_stock', {'total_qtd':'total_qtd + '+qtd}, {'code':code})
        return True

    def addLot(self, code, data, qtd, cost, db):
        db.insert('tb_lot', ['code', 'dt_buy', 'qtd', 'cost'], [code, data, qtd, cost])
        return True

    def removeLot(self, id, db):
        db.delete('tb_lot', {'id':id} )
        return True
