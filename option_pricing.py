

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
    premium = 100
    
    stock = Stock(10, 1100, 0.4, 0.6)
    
    

    for i in range(10):
        print(call(stock, premium))
        print('-'*60)
        stock.prob_up += 0.05
        stock.prob_down -= 0.05


def call(stock, premium):
    ans = int(stock.expected_payoff(premium))
    if ans > 0:
        return f'Stock:\n\tPrice: {stock.price}\n\tCount: {stock.count}\nIt\'s Favourable! The expected payoff is {ans}.'
    elif ans == 0:
        return f'\n\t- It\'s a Fair Deal, the expected payoff is {ans}.'
    else:
        return f'\n\t- It\'s Bad! The expected payoff is {ans}.'
        



if __name__ == '__main__':
    main()