"""This is being started 7/21/25, near the end of my course
at Georgia Tech - CS 7646 Machine Learning for Trading.

I wanted to try different structures to solutions I've already
made to see if I can simplify experimentation.
"""
import logging
import polars as pl
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod


class Indicator(metaclass=ABCMeta):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Avoid adding multiple handlers if already present
        if not self.logger.handlers:
            self.logger.addHandler(handler)

        self._values = None

    @property
    def values(self):
        return self._values

    def _set_values(self, val):
        self._values = val

    @abstractmethod
    def compute(self, data:pl.Series) -> pl.Series:
        pass

    @abstractmethod
    def plot(self, show=True, save_location='') -> None:
        pass


# --- Indicator Subclasses ---

class PercentBollingerBands(Indicator):
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, data:pl.Series, span:int=20) -> pl.Series:
        try:
            if not isinstance(data, pl.Series):
                raise TypeError("Data must be a polars Series.")
            if data.is_empty():
                raise ValueError("Data Series is empty.")
            if span <= 0:
                raise ValueError("Span must be a positive integer.")
            ema = data.ewm_mean(span=span)
            std = data.ewm_std(span=span)

            upper_band = ema + (std * 2)
            lower_band = ema - (std * 2)

            eps = 1e-12
            self._set_values((data - lower_band) / ((upper_band - lower_band) + eps))
            self.logger.info("Computed Percent Bollinger Bands successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise

        return self.values
    
    def plot(self, normalized=True, show=True, save_location='') -> None:
        if normalized:
            data:pl.Series = self.values / self.values[0]
        else:
            data:pl.Series = self.values

        if show:
            # Convert to pandas for plotting
            data.to_pandas().plot()
            plt.title("Percent Bollinger Bands")
            plt.xlabel("Time")
            plt.ylabel("PBB Value")
            plt.show()

        if save_location:
            plt.savefig(save_location)


class Momentum(Indicator):
    """
    Momentum indicator (Rate of Change):
    Computes the rate of change between an exponential moving average (EMA) and a simple moving average (SMA):
        ROC = ((EMA - SMA) / SMA) * 100
    Default: EMA span=10, SMA window=30
    """
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, data: pl.Series, span: int = 10, window: int = 30) -> pl.Series:
        try:
            if not isinstance(data, pl.Series):
                raise TypeError("Data must be a polars Series.")
            if data.is_empty():
                raise ValueError("Data Series is empty.")
            if span <= 0 or window <= 0:
                raise ValueError("Span and window must be positive integers.")
            if len(data) <= window:
                raise ValueError("Data length must be greater than window.")
            ema = data.ewm_mean(span=span)
            sma = data.rolling_mean(window_size=window)
            eps = 1e-12
            roc = ((ema - sma) / (sma + eps)) * 100
            self._set_values(roc)
            self.logger.info("Computed Momentum (ROC) successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("Momentum (ROC)")
            plt.xlabel("Time")
            plt.ylabel("Momentum Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class RSI(Indicator):
    """Relative Strength Index (RSI) indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, data: pl.Series, window: int = 14) -> pl.Series:
        try:
            if not isinstance(data, pl.Series):
                raise TypeError("Data must be a polars Series.")
            if data.is_empty():
                raise ValueError("Data Series is empty.")
            delta = data.diff()
            gain = delta.clip(lower_bound=0)
            loss = -delta.clip(upper_bound=0)
            avg_gain = gain.ewm_mean(span=window)
            avg_loss = loss.ewm_mean(span=window)
            eps = 1e-12
            rs = avg_gain / (avg_loss + eps)
            rsi = 100 - (100 / (1 + rs))
            self._set_values(rsi)
            self.logger.info("Computed RSI successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("RSI")
            plt.xlabel("Time")
            plt.ylabel("RSI Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class MACD(Indicator):
    """Moving Average Convergence Divergence (MACD) indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, data: pl.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pl.DataFrame:
        try:
            if not isinstance(data, pl.Series):
                raise TypeError("Data must be a polars Series.")
            if data.is_empty():
                raise ValueError("Data Series is empty.")
            ema_fast = data.ewm_mean(span=fast)
            ema_slow = data.ewm_mean(span=slow)
            macd = ema_fast - ema_slow
            signal_line = macd.ewm_mean(span=signal)
            hist = macd - signal_line
            df = pl.DataFrame({"macd": macd, "signal": signal_line, "hist": hist})
            self._set_values(df)
            self.logger.info("Computed MACD successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        df = self.values
        if show and isinstance(df, pl.DataFrame):
            df.select(["macd", "signal", "hist"]).to_pandas().plot()
            plt.title("MACD")
            plt.xlabel("Time")
            plt.ylabel("MACD Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class SMACrossover(Indicator):
    """Simple Moving Average Crossover indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, data: pl.Series, short: int = 20, long: int = 50) -> pl.Series:
        try:
            if not isinstance(data, pl.Series):
                raise TypeError("Data must be a polars Series.")
            if data.is_empty():
                raise ValueError("Data Series is empty.")
            sma_short = data.rolling_mean(window_size=short)
            sma_long = data.rolling_mean(window_size=long)
            crossover = sma_short - sma_long
            self._set_values(crossover)
            self.logger.info("Computed SMA Crossover successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("SMA Crossover")
            plt.xlabel("Time")
            plt.ylabel("Crossover Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class ATR(Indicator):
    """Average True Range (ATR) indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, high: pl.Series, low: pl.Series, close: pl.Series, window: int = 14) -> pl.Series:
        try:
            tr1 = (high - low).abs()
            tr2 = (high - close.shift(1)).abs()
            tr3 = (low - close.shift(1)).abs()
            tr_df = pl.DataFrame({"tr1": tr1, "tr2": tr2, "tr3": tr3})
            tr = tr_df.select(pl.max_horizontal(pl.all()).alias("tr"))["tr"]
            atr = tr.rolling_mean(window_size=window)
            self._set_values(atr)
            self.logger.info("Computed ATR successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("ATR")
            plt.xlabel("Time")
            plt.ylabel("ATR Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class OBV(Indicator):
    """On-Balance Volume (OBV) indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, close: pl.Series, volume: pl.Series) -> pl.Series:
        try:
            direction = close.diff().fill_null(0).sign()
            obv = (volume * direction).cum_sum()
            self._set_values(obv)
            self.logger.info("Computed OBV successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("OBV")
            plt.xlabel("Time")
            plt.ylabel("OBV Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class CCI(Indicator):
    """Commodity Channel Index (CCI) indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, high: pl.Series, low: pl.Series, close: pl.Series, window: int = 20) -> pl.Series:
        try:
            tp = (high + low + close) / 3
            sma = tp.rolling_mean(window_size=window)
            mad = (tp - sma).abs().rolling_mean(window_size=window)
            eps = 1e-12
            cci = (tp - sma) / (0.015 * (mad + eps))
            self._set_values(cci)
            self.logger.info("Computed CCI successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("CCI")
            plt.xlabel("Time")
            plt.ylabel("CCI Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class WilliamsR(Indicator):
    """Williams %R indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, high: pl.Series, low: pl.Series, close: pl.Series, window: int = 14) -> pl.Series:
        try:
            highest_high = high.rolling_max(window_size=window)
            lowest_low = low.rolling_min(window_size=window)  # fixed (was rolling_max)
            eps = 1e-12
            willr = -100 * (highest_high - close) / ((highest_high - lowest_low) + eps)
            self._set_values(willr)
            self.logger.info("Computed Williams %R successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("Williams %R")
            plt.xlabel("Time")
            plt.ylabel("%R Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class ParabolicSAR(Indicator):
    """Parabolic SAR indicator (simplified version)."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, high: pl.Series, low: pl.Series, close: pl.Series, step: float = 0.02, max_step: float = 0.2) -> pl.Series:
        # Note: A full Parabolic SAR implementation is complex; this is a placeholder.
        try:
            # Placeholder: just return close for now
            self._set_values(close)
            self.logger.info("Computed Parabolic SAR (placeholder) successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("Parabolic SAR (placeholder)")
            plt.xlabel("Time")
            plt.ylabel("SAR Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class VWAP(Indicator):
    """Volume Weighted Average Price (VWAP) indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, price: pl.Series, volume: pl.Series) -> pl.Series:
        try:
            vwap = (price * volume).cum_sum() / volume.cum_sum()
            self._set_values(vwap)
            self.logger.info("Computed VWAP successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("VWAP")
            plt.xlabel("Time")
            plt.ylabel("VWAP Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)


class CMF(Indicator):
    """Chaikin Money Flow (CMF) indicator."""
    def __init__(self):
        super().__init__()
        self._set_values(pl.Series())

    def compute(self, high: pl.Series, low: pl.Series, close: pl.Series, volume: pl.Series, window: int = 20) -> pl.Series:
        try:
            eps = 1e-12
            denom = (high - low)
            mf_multiplier = ((close - low) - (high - close)) / (denom + eps)
            mf_volume = mf_multiplier * volume
            cmf = mf_volume.rolling_sum(window_size=window) / (volume.rolling_sum(window_size=window) + eps)
            self._set_values(cmf)
            self.logger.info("Computed CMF successfully.")
        except Exception:
            self.logger.exception("Error in compute:")
            raise
        return self.values

    def plot(self, show=True, save_location='') -> None:
        data = self.values
        if show:
            data.to_pandas().plot()
            plt.title("CMF")
            plt.xlabel("Time")
            plt.ylabel("CMF Value")
            plt.show()
        if save_location:
            plt.savefig(save_location)
