import polars as pl
import Indicators as ind

def build_features_from_ohlcv(close: pl.Series, high: pl.Series, low: pl.Series, volume: pl.Series) -> pl.DataFrame:
    # Instantiate indicators
    pbb = ind.PercentBollingerBands().compute(close).alias("pbb")
    mom = ind.Momentum().compute(close).alias("mom")
    rsi = ind.RSI().compute(close).alias("rsi")
    macd_df = ind.MACD().compute(close).rename({"macd":"macd","signal":"macd_signal","hist":"macd_hist"})
    sma_x = ind.SMACrossover().compute(close).alias("sma_x")
    atr = ind.ATR().compute(high, low, close).alias("atr")
    obv = ind.OBV().compute(close, volume).alias("obv")
    cci = ind.CCI().compute(high, low, close).alias("cci")
    willr = ind.WilliamsR().compute(high, low, close).alias("willr")
    vwap = ind.VWAP().compute(close, volume).alias("vwap")
    cmf = ind.CMF().compute(high, low, close, volume).alias("cmf")

    df = pl.DataFrame({
        "close": close, "high": high, "low": low, "volume": volume,
        "pbb": pbb, "mom": mom, "rsi": rsi, "sma_x": sma_x,
        "atr": atr, "obv": obv, "cci": cci, "willr": willr,
        "vwap": vwap, "cmf": cmf
    }).hstack(macd_df)

    # Drop rows with any nulls produced by rolling/ewm
    df = df.drop_nulls()

    # Add 1-period log return for reward
    df = df.with_columns(pl.col("close").log().diff().alias("ret1")).drop_nulls()

    return df
