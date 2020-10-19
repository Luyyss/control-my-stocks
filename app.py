import src.utils.functions as funcs
from src.classes.DataBase import DataBase
from src.utils.defaults import variables as va
from src.classes.StockControll import StockControll
from flask import Flask, redirect, url_for, render_template, jsonify, request


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

@app.route('/app/data')
def getData():

    # all_stocks = [['ITSA4', 111], ['BBSE3', 25], ['CIEL3', 225], ['BIDI4', 15]]
    all_stocks = db.select('tb_stock', ['code', 'name', 'total_qtd'])
    all_lots = db.select('tb_lot')

    data = {
        'stocks': [],
        'lots': all_lots,
        'info':{
            'total':0,
            'result':0
        }
    }

    for stock, name, amount in all_stocks:
        aux = funcs.getStockInfo( stock )
        aux['code'] = stock
        aux['name'] = name
        aux['amount'] = amount
        data['stocks'].append( aux )
        data['info']['total'] += float(aux['price']) * int(amount)

    return jsonify(data)


@app.route('/app/stocks')
def getStocks():

    # return jsonify( funcs.getAllStocksSymbols() )
    return jsonify( funcs.readStocksFile() )


@app.route('/app/new', methods=['POST'])
def newStock():

    if request.method == "POST":

        stock = request.form['stock']

        code, name = stock.split(' | ')

        data = {}
        stc = StockControll()

        if len(stock) > 0:
            # redirect(url_for('dashboard'))
            stc.addStock(code, name, db)
            data['status'] = 'ok'
        else:
            data['status'] = 'erro'

        return jsonify(data)


@app.route('/app/remove', methods=['POST'])
def removeStock():

    if request.method == "POST":

        stc = StockControll()
        stock = request.form['stock']
        stc.removeStock(stock, db)

        data = {'status':'ok'}
        return jsonify(data)


@app.route('/app/lot', methods=['POST'])
def newLot():

    if request.method == "POST":

        stock = request.form['stock']
        data = request.form['data']
        qtd = request.form['qtd']
        preco = request.form['preco']

        stc = StockControll()
        stc.addLot(stock, data, qtd, preco, db)
        stc.updateTotal(stock, qtd, db)

        data = {'status':'ok'}
        return jsonify(data)

@app.route('/app/lot', methods=['DELETE'])
def removeLot():

    if request.method == "DELETE":

        StockControll().removeLot( request.form['id'], db)

        data = {'status':'ok'}
        return jsonify(data)

if __name__ == '__main__':
    app.run()