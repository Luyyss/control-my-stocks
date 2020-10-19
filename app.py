import src.utils.functions as funcs
from src.utils.database import database
from src.utils.defaults import variables as va
from flask import Flask, redirect, url_for, render_template, jsonify, request


db = database(va['DATABASE'])

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
    all_stocks = []

    data = {
        'stocks':[],
        'info':{
            'total':0,
            'result':0
        }
    }

    for stock, amount in all_stocks:
        aux = funcs.getStockInfo( stock )
        aux['amount'] = amount
        data['stocks'].append( aux )

    for stock in data['stocks']:
        data['info']['total'] += float(stock['price']) * int(stock['amount'])

    return jsonify(data)


@app.route('/app/stocks')
def getStocks():

    data = funcs.getAllStocksSymbols()
    return jsonify(data)


@app.route('/app/new', methods=['POST'])
def newStock():

    if request.method == "POST":

        from src.class.StockControll import StockControll

        stock = request.form['stock']

        code, name = stock.split(' | ')

        data = {}

        if len(stock) > 0:
            # redirect(url_for('dashboard'))
            StockControll. addStock(code, name, db)
            data['status'] = 'ok'
        else:
            data['status'] = 'erro'

        return jsonify(data)

if __name__ == '__main__':
    app.run()