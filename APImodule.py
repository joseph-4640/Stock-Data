import pandas as pd
import requests
import sqlite3

class AlphaVantageAPI:
    """AlphaVantage API class for extracting stock data."""
    
    def __init__(self, api_key="PGPVDW57277TSFM3"):
        self.api_key=api_key
        
    def get_daily(self, ticker, output_size="full"):
        """Get daily time series of an equity from AlphaVantage.
        parameters
        _ _ _ _ _ _
        ticker: str
            The ticker symbol of the equity.
        output_size: str
            Number of observations to return. "full" means the historic observations of the equtiy to be returned, "compact means the most recent observations."
        returns
        _ _ _ _ _ _
        pd.DataFrame:
            Columns are "open, high, low, close, volume"
        """
        
        # Create URL
        url = (
            "https://www.alphavantage.co/query?"
            "function=TIME_SERIES_DAILY&"
            f"symbol={ticker}&"
            f"outputsize={output_size}&"
            f"datatype=json&"
            f"apikey={self.api_key}&"
        )
        
        # Send request to api
        response = requests.get(url=url)
        
        # Check if the request  is successfull
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code}")
        
        # Extract JSON data from response
        response_data = response.json()
        
        # Check if the "Time Series key exists" in response_data
        if "Time Series (Daily)" not in response_data.keys():
            raise Exception(
                f"Invalid API call. Check the ticker symbol: {ticker}"
            )
        
        # Extract json data from response
        data = response_data["Time Series (Daily)"]
        
        # Read data into DataFrame
        stock_data = pd.DataFrame.from_dict(data, orient="index", dtype="float")
        
        # Convert "index" to "datetime index" and name "date"
        stock_data.index =  pd.to_datetime(stock_data.index)
        stock_data.index.name = "date"

        # Removing numbering from your column names
        stock_data.columns = [c.split(".")[1] for c in stock_data.columns]
        
        return stock_data
    
    
    
    
