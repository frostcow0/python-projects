

import logging
import pandas as pd
import csv
import requests
from io import StringIO


class Stock:
    """
    Represents a stock and provides methods to pull its latest and historical data.
    """
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.latest_data = None
        self.historical_data = None

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)



    def fetch_latest(self):
        """Pulls the latest available data for the stock and stores it in self.latest_data."""
        self.latest_data = self._pull_current(self.symbol, self.logger)
        return self.latest_data


    def fetch_historical(self):
        """Pulls recent historical data for the stock and stores it in self.historical_data."""
        self.historical_data = self._pull_historical(self.symbol, self.logger)
        return self.historical_data



    @staticmethod
    def _pull_current(stock, logger=None):
        """
        Fetches the latest intraday data for the given stock symbol.
        Returns a dict of parsed data, or None on failure.
        """
        stock_url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}?'
        params = {
            'region': 'US',
            'range': '1d',
            'interval': '5m',
            'includeTimestamps': 'false'
        }
        try:
            response = requests.get(stock_url.format(stock), params=params, timeout=10)
            response.raise_for_status()
            file = StringIO(response.text)
            reader = csv.reader(file)
            data = list(reader)
            if not data or len(data[0]) < 12:
                if logger:
                    logger.error(f"Malformed or empty data for {stock} in _pull_current.")
                return None
            result = {
                data[0][9][:18]: data[0][9][19:],
                data[0][11][:13]: data[0][11][14:]
            }
            if logger:
                logger.info(f"Fetched current data for {stock} successfully.")
            return result
        except Exception as e:
            if logger:
                logger.exception(f"Error fetching current data for {stock}:")
            else:
                print(f"Error fetching current data for {stock}: {e}")
            return None



    @staticmethod
    def _pull_historical(stock, logger=None):
        """
        Fetches recent historical daily data for the given stock symbol.
        Returns a DataFrame, or an empty DataFrame on failure.
        """
        stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?'
        params = {
            'range': '7d',
            'interval': '1d',
            'events': 'history'
        }
        try:
            response = requests.get(stock_url.format(stock), params=params, timeout=10)
            response.raise_for_status()
            file = StringIO(response.text)
            df = pd.read_csv(file)
            if logger:
                logger.info(f"Fetched historical data for {stock} successfully.")
            return df
        except Exception as e:
            if logger:
                logger.exception(f"Error fetching historical data for {stock}:")
            else:
                print(f"Error fetching historical data for {stock}: {e}")
            return pd.DataFrame()

    def __repr__(self):
        return f"<Stock {self.symbol}>"
