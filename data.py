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
    
    
class SQLRepository:
    """ SQLRepository class for data storage. """
    
    def __init__(self, connection):
        self.connection = connection
        
    def insert_table(self, table_name, records, if_exists="fill"):
        """
        Create a sample table if it doesn't exists.
        parameters
        ---------
        table_name:
           The name of the table where you want to insert records.
        records: 
           A list of tuples containing the data you want to insert. Each tuple represents a single record.
        if_exists: 
           A string that defines the behavior if the records already exist. It can be "fill" to insert new records or "replace" to delete existing records with the same ID before inserting.
        Returns
        ---------
        dict
           A dictionary with transaction success status and number of records inserted.
        """
        
        n_inserted = records.to_sql(name=table_name, con=self.connection, if_exists=if_exists)
        
        return {
            "transaction_successful": True,
            "records_inserted": n_inserted
        }
        
        
    def read_table(self, table_name, limit=2500):
        """
        Retrieves data from a specified database table and returns it as a pandas DataFrame.
        parameters
        ----------
        table_name (str):
            The name of the database table from which to read data. The table should exist in the connected database.

        limit (int):
                The maximum number of rows to return from the table. Defaults to 2500. This is useful for limiting data fetched for analysis, especially with large datasets.
                
        Returns
        ---------
        DataFrame:
                A pandas DataFrame containing the data retrieved from the specified table, limited to the specified number of rows.
        """
        
        # Create query with 'optional limit'
        if limit:
            sql_query = f"SELECT * FROM '{table_name}' LIMIT {limit}"
        else:
            sql_query = f"SELECT * FROM '{table_name}'"
        
        # Retrive data and read into dataframe
        df = pd.read_sql(
            sql_query,
            con=self.connection,
            parse_dates=["date"],
            index_col="date"
        )
        
        return df
    
