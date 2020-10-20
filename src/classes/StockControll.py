from src.classes.Stock import Stock

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
        self.__calculeAvgPrice(code, db)
        return True

    def removeLot(self, id, db):
        db.delete('tb_lot', {'id':id} )
        return True

    def __calculeAvgPrice(self, code, db):
        # res = db.select('tb_stock', None, {'code':code})[0]
        # stock = Stock(res[0], res[1], res[2], res[3], res[1] )
        res = db.select('tb_lot', ['qtd', 'cost'], {'code':code})

        sumQtd = 0
        amount = 0

        print(res)

        for qtd, cost in res:
            sumQtd += int(qtd)
            amount += int(qtd) * float(cost)

        avg = amount / sumQtd

        print(sumQtd)
        print(amount)
        print(avg)
        # ((stock.qtd * stock.avg) + ( * ) ) / ( + )
