import src.utils.functions as funcs
from src.classes.DataBase import DataBase
from src.utils.defaults import variables as va
from src.classes.StockControll import StockControll
from flask import Flask, session, render_template, jsonify, request
import os

db = DataBase('postgres://cbolmnrxydramg:f6dd6b3e65549a0cf705fcaacd383de68a39edb1413bd69fd60be6c91e1fc8b7@ec2-3-218-75-21.compute-1.amazonaws.com:5432/dehskavu22md39')
# db = DataBase(os.getenv('DATABASE_URL'))

app = Flask(__name__, template_folder='src/pages')

app.config.update(
    #TESTING=True,
    TEMPLATES_AUTO_RELOAD=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/app/data', methods=['GET'])
def getData():

    all_stocks = db.select('tb_stock', ['code', 'total_qtd'])
    return jsonify(all_stocks)

@app.route('/app/prices', methods=['GET'])
def getPrices():

    all_stocks = db.select('tb_stock', ['code', 'name', 'total_qtd', 'avg_cost'])

    data = {
        'stocks': [],
        'lots': [],
        'info':{
            'total_paid':0,
            'total_today':0,
            'result':0,
            'result_percent':0
        }
    }

    if len(all_stocks) > 0:
        all_lots = db.select('tb_lot')

        data['lots'] = all_lots

        stc = StockControll()

        for stock, name, amount, avg_cost in all_stocks:
            aux = funcs.getStockInfo( stock.strip() )
            aux['code'] = stock.strip()
            aux['name'] = name
            aux['total_qtd'] = amount
            aux['avg_cost'] = avg_cost
            aux['resume'] = stc.calculeResume(aux)
            data['stocks'].append( aux )
            data['info']['total_today'] += float(aux['price']) * int(amount)
            data['info']['total_paid'] += float(avg_cost) * int(amount)

        if data['info']['total_paid'] > 0 and data['info']['total_today'] > 0:
            data['info']['result'] = funcs.formatFloat( data['info']['total_today'] - data['info']['total_paid'] )
            data['info']['result_percent'] = funcs.formatFloat( (data['info']['result'] / data['info']['total_paid']) * 100 )

        data['info']['refresh'] = funcs.validCurrentTime()

    return jsonify(data)


@app.route('/app/stocks', methods=['GET'])
def getStocks():
    return jsonify( funcs.readStocksFile() )


@app.route('/app/stock', methods=['POST', 'DELETE'])
def newStock():

    data = {'status':''}

    if request.method == "POST":

        stock = request.form['stock']

        code, name = stock.split(' | ')

        stc = StockControll()

        if len(stock) > 0:
            stc.addStock(code.strip(), name, db)
            data['status'] = 'ok'
        else:
            data['status'] = 'erro'

    elif request.method == "DELETE":

        stc = StockControll()
        stock = request.form['stock']
        stc.removeStock(stock, db)

        data['status'] = 'ok'

    return jsonify(data)

@app.route('/app/lot', methods=['POST', 'DELETE'])
def newLot():

    if request.method == "POST":

        stock = request.form['stock']
        data = request.form['data']
        qtd = request.form['qtd']
        preco = request.form['preco'].replace('.','').replace(',','.')

        stc = StockControll()
        stc.addLot(stock, data, qtd, preco, db)
        stc.calculeStatsFromLots(stock, db)

        data = {'status':'ok'}
        return jsonify(data)

    elif request.method == "DELETE":

        stc = StockControll()
        stc.removeLot( request.form['id'], db)
        stc.calculeStatsFromLots(request.form['stock'], db)

        data = {'status':'ok'}
        return jsonify(data)


if __name__ == '__main__':
    app.run()