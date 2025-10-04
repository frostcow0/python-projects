import polars as pl
import yfinance as yf
import Indicators as ind
from pathlib import Path
from features import build_features_from_ohlcv

def fetch_ohlcv(ticker_symbol: str, period: str = "10y", interval: str = "1d"):
    hist = yf.Ticker(ticker_symbol).history(period=period, interval=interval, auto_adjust=True)
    close = pl.Series("close", hist["Close"].values)
    high  = pl.Series("high",  hist["High"].values)
    low   = pl.Series("low",   hist["Low"].values)
    vol   = pl.Series("volume",hist["Volume"].values)
    return close, high, low, vol

def main():
    ticker = "MSFT"
    close, high, low, vol = fetch_ohlcv(ticker, period="10y", interval="1d")
    feats = build_features_from_ohlcv(close, high, low, vol)
    out = Path(f"{ticker}_features.parquet")
    feats.write_parquet(out.as_posix())
    print("Wrote features to:", out)
    print(feats.head(5))

if __name__ == "__main__":
    main()
