import src.utils.functions as funcs
from src.classes.DataBase import DataBase
from src.utils.defaults import variables as va
from src.classes.StockControll import StockControll
from flask import Flask, session, render_template, jsonify, request


db = DataBase(va['DATABASE'])

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

    all_stocks = db.select('tb_stock', ['code', 'name', 'total_qtd', 'avg_cost'])
    return jsonify(all_stocks)

@app.route('/app/prices', methods=['GET'])
def getPrices():

    all_stocks = db.select('tb_stock', ['code', 'name', 'total_qtd', 'avg_cost'])
    all_lots = db.select('tb_lot')

    data = {
        'stocks': [],
        'lots': all_lots,
        'info':{
            'total_paid':0,
            'total_today':0,
            'result':0,
            'result_percent':0
        }
    }

    stc = StockControll()

    for stock, name, amount, avg_cost in all_stocks:
        aux = funcs.getStockInfo( stock )
        aux['code'] = stock
        aux['name'] = name
        aux['total_qtd'] = amount
        aux['avg_cost'] = avg_cost
        aux['resume'] = stc.calculeResume(aux)
        data['stocks'].append( aux )
        data['info']['total_today'] += float(aux['price']) * int(amount)
        data['info']['total_paid'] += float(avg_cost) * int(amount)

    data['info']['result'] = data['info']['total_today'] - data['info']['total_paid']
    data['info']['result_percent'] = funcs.formatFloat( (data['info']['result'] / data['info']['total_paid']) * 100 )

    data['info']['result'] = funcs.formatFloat(data['info']['result'])
    data['info']['refresh'] = funcs.validCurrentTime()

    return jsonify(data)


@app.route('/app/stocks', methods=['GET'])
def getStocks():

    # return jsonify( funcs.getAllStocksSymbols() )
    return jsonify( funcs.readStocksFile() )


@app.route('/app/stock', methods=['POST', 'DELETE'])
def newStock():

    data = {'status':''}

    if request.method == "POST":

        stock = request.form['stock']

        code, name = stock.split(' | ')

        stc = StockControll()

        if len(stock) > 0:
            # redirect(url_for('dashboard'))
            stc.addStock(code, name, db)
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
        preco = request.form['preco']

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