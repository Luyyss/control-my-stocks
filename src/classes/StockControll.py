from src.classes.Stock import Stock
import src.utils.functions as funcs

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

    def calculeStatsFromLots(self, code, db):
        res = db.select('tb_lot', ['qtd', 'cost'], {'code':code})

        sumQtd = 0
        amount = 0

        for qtd, cost in res:
            sumQtd += int(qtd)
            amount += int(qtd) * float(cost)

        avg = 0 if amount == 0 or sumQtd == 0 else funcs.formatFloat(amount / sumQtd, 5)

        db.update('tb_stock', {'total_qtd':sumQtd, 'avg_cost':avg}, {'code':code})

        return True #amount, sumQtd, avg

    def calculeResume(self, data):
        amount = int(data['total_qtd'])

        if amount > 0:
            price = float(data['price'])
            avg_cost = float(data['avg_cost'])

            totalInStock = avg_cost * amount
            totalNow = price * amount

            dif = totalNow - totalInStock
            percent = (dif / totalInStock) * 100

            return [ funcs.formatFloat(dif), funcs.formatFloat(percent) ]

        else:
            return ['----', '-----']