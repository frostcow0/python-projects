import Indicators as ind
import polars as pl
import pandas as pd
import yfinance as yf

def evaluate_indicators(ticker_symbol):
    # Fetch historical data
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="1y", interval="1d")
    close = pl.Series("close", hist["Close"].values)
    high = pl.Series("high", hist["High"].values)
    low = pl.Series("low", hist["Low"].values)
    volume = pl.Series("volume", hist["Volume"].values)

    # Compute indicators
    indicators = {}

    # Percent Bollinger Bands
    pbb = ind.PercentBollingerBands()
    indicators['PercentBollingerBands'] = pbb.compute(close)

    # Momentum
    momentum = ind.Momentum()
    indicators['Momentum'] = momentum.compute(close)

    # RSI
    rsi = ind.RSI()
    indicators['RSI'] = rsi.compute(close)

    # MACD
    macd = ind.MACD()
    indicators['MACD'] = macd.compute(close)

    # SMA Crossover
    sma_cross = ind.SMACrossover()
    indicators['SMACrossover'] = sma_cross.compute(close)

    # ATR
    atr = ind.ATR()
    indicators['ATR'] = atr.compute(high, low, close)

    # OBV
    obv = ind.OBV()
    indicators['OBV'] = obv.compute(close, volume)

    # CCI
    cci = ind.CCI()
    indicators['CCI'] = cci.compute(high, low, close)

    # Williams %R
    willr = ind.WilliamsR()
    indicators['WilliamsR'] = willr.compute(high, low, close)

    # VWAP
    vwap = ind.VWAP()
    indicators['VWAP'] = vwap.compute(close, volume)

    # CMF
    cmf = ind.CMF()
    indicators['CMF'] = cmf.compute(high, low, close, volume)

    # Print or plot results
    for name, result in indicators.items():
        print(f"{name}:")
        print(result)
        print("-" * 40)
        # Optionally: indicators[name].plot()

def main():
    evaluate_indicators("MSFT")

if __name__ == '__main__':
    main()