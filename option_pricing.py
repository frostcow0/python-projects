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
    data = []
    columns = ['rating', 'payoff', 'price', 'count', 'p(u)', 'p(d)']
    premium = 100
    stock = Stock(10, 1100, 0.4, 0.6)
    for i in range(10):
        data.append(call(stock, premium))
        # print('-'*60)
        stock.prob_up -= 0.05
        stock.prob_down += 0.05
    df = pd.DataFrame(data=data, columns=columns)
    print(df)

def call(stock, premium):
    ans = int(stock.expected_payoff(premium))
    if ans > 0:
        # print(f'Stock:\n\tPrice: {stock.price}\n\tCount: {stock.count}\n\tP(Up): {stock.prob_up}\n\tP(Down): {stock.prob_down}\nIt\'s Favourable! The expected payoff is {ans}.')
        return ['good', ans, stock.price, stock.count, round(stock.prob_up, 2), round(stock.prob_down, 2)]
    elif ans == 0:
        # print(f'Stock:\n\tPrice: {stock.price}\n\tCount: {stock.count}\n\tP(Up): {stock.prob_up}\n\tP(Down): {stock.prob_down}\nIt\'s a Fair Deal, the expected payoff is {ans}.')
        return ['fair', ans, stock.price, stock.count, round(stock.prob_up, 2), round(stock.prob_down, 2)]
    else:
        # print(f'Stock:\n\tPrice: {stock.price}\n\tCount: {stock.count}\n\tP(Up): {stock.prob_up}\n\tP(Down): {stock.prob_down}\nIt\'s Bad! The expected payoff is {ans}.')
        return ['bad', ans, stock.price, stock.count, round(stock.prob_up, 2), round(stock.prob_down, 2)]
        
if __name__ == '__main__':
    main()