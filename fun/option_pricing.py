import pandas as pd

class Stock():
    def __init__(self, count, price, prob_up, prob_down):
        self.count = count
        self.price = price
        self.prob_up = prob_up
        self.prob_down = prob_down
        self.fall_amt = self.price-100
        self.up_amt = self.price+100

    def expected_payoff(self, premium):
        expected = self.prob_down*(self.fall_amt-self.price)+self.prob_up*((self.up_amt*self.count)-(self.price*self.count)-premium)
        return expected

def main(args=None):
    count = 10
    price = 1100
    p_u = 0.4
    p_d = 0.6
    premium = 100

    data = []
    columns = ['rating', 'payoff', 'price', 'count', 'p(u)', 'p(d)']
    stock = Stock(count, price, p_u, p_d)
    for i in range(10):
        data.append(call(stock, premium))
        stock.prob_up -= 0.05
        stock.prob_down += 0.05
    df = pd.DataFrame(data=data, columns=columns)
    print(df)

def call(stock, premium):
    ans = int(stock.expected_payoff(premium))
    if ans > 0:
        return ['good', ans, stock.price, stock.count, round(stock.prob_up, 2), round(stock.prob_down, 2)]
    elif ans == 0:
        return ['fair', ans, stock.price, stock.count, round(stock.prob_up, 2), round(stock.prob_down, 2)]
    else:
        return ['bad', ans, stock.price, stock.count, round(stock.prob_up, 2), round(stock.prob_down, 2)]
        
if __name__ == '__main__':
    main()