
class Stock:

    def __init__(self, code, name=None, qtd=0, price=0, avg_cost=0, balance=None):
        self.qtd = qtd
        self.code = code
        self.name = name
        self.price = price
        self.balance = balance
        self.avg_cost = avg_cost
        