import pandas as pd
from glob import glob
from data import SQLRepository
from data import AlphaVantageAPI
from arch import arch_model
import sqlite3
import os
import joblib
from settings import model_directory


class GarchModel:
    """ Garch model class with methods for wrangling data, training, predicting, serving and loading models.
    """
    
    def __init__(self, ticker, repo, use_new_data):
        self.ticker=ticker
        self.repo=repo
        self.use_new_data=use_new_data
        self.model_directory = model_directory
    
    def wrangle_data(self, n_observations):
        """
        Extract data from the database(or get from AlphaVantage API). Transform it for training model, and attach it to self.data

        Args:
            n_observations (int): Number of observations to retrieve from database.
        
        Returns:
            returns None
        """
        
        # Add new data to database if requuired
        if self.use_new_data:
            # Instantiate an API class
            api = AlphaVantageAPI()
            
            # Get data
            new_data = api.get_daily(ticker=self.ticker)
            
            # Insert data into database
            self.repo.insert_table(
                table_name = self.ticker, records=new_data, if_exists="replace"
            )
            
        # Pull data from SQL database
        df = self.repo.read_table(table_name=self.ticker, limit=n_observations + 1)
            
        # Clean data, attach to class as 'data' attribute
        df.sort_index(ascending=True, inplace=True)
            
        # Create return column
        df["return"] = df[" close"].pct_change() * 100
            
        self.data = df["return"].dropna()
        
        
    def fit(self, p, q):
        """ Create model, fit to self.data, and attach to self.model attribute.
        For assignment also assigns adds metrics to 'self.arc' and 'self.bic'

        Args:
            p (int): Lag order of symmetric innovation.
            q (int): Lag oder of lagged volatility.
        
        Returns:
            None
        """
        
        # Train model, attatch to self.model
        self.model = arch_model(self.data, p=p, q=q, rescale=False).fit(disp=0)
        
    
    def __clean_prediction(self, prediction):
        """ Reformat model predictions to JSON

        Args:
            prediction (pd.DataFrame: Variance from GARCH model forecast
        
        Returns:
            dict: Forecast of volatility. Each key is date in ISO-8601 format. Each value is predicted volatility.
        """
        
        # Access forecasted variance (last row contains the horizon forecast)
        prediction = self.model.forecast(horizon=5, reindex=False).variance ** 0.5  # Variance for the forecast horizon
        
        # Calculate forecast start date (one day after the last date in the original data)
        start = prediction.index[0] + pd.DateOffset(days=1)  # Replace with actual forecast start date
        
        # Create date range for forecast horizon
        prediction_dates = pd.bdate_range(start=start, periods=prediction.shape[1])  # Business days
        
        # Create prediction index labels in ISO-8601 format
        prediction_index = [d.isoformat() for d in prediction_dates]

        # Extract the predictions from dataframe, get square root
        data = prediction.values.flatten() ** 0.5
        
        # Combine data and prediction index into a series
        prediction_formatted = pd.Series(data, index=prediction_index)
        
        # Return series as a dictionary
        prediction_formatted.to_dict()
        
        # Return the formatted prediction as a dictionary
        return prediction_formatted
    
    
    def predict_volatility(self, horizon):
        """ Predict volatility using "self.model"

        Args:
            horizon (int)): Horizon of forecast
        Returns:
            dict: Forecast of volatility. Each key is a date in ISO-8601 format. Each value is predicted volatility.
        """
        
        # Generate variance forecast from 'self.model'
        prediction = self.model.forecast(horizon=horizon, reindex=False).variance
        
        # Format prediction with 'self.__clean_prediction'
        prediction_formatted = self.__clean_prediction(prediction)
        
        return prediction_formatted
    
    def dump(self):
        """ Save model to 'self.model_directory' with timestamp.
        Returns:
            str: filepath where the model is saved
        """
        
        # Create timestamp in ISO-8601 format
        timestamp = pd.Timestamp.now().isoformat()
        
        # Create a filepath, including 'self.model_directory'
        filepath = os.path.join(self.model_directory, f"{timestamp}_{self.ticker}.pkl")
        
         # Check if the directory exists, and create it if it doesn't
        if not os.path.exists(self.model_directory):
            os.makedirs(self.model_directory)
        
        # Save 'self.model'
        joblib.dump(self.model, filepath)
        
        # Return filepath
        return filepath
    
    
    def load(self):
        """ Load latest model from model in 'self.model_directory'
        for 'self.ticker', attatch to 'self.model' attribute

        Args:
            ticker (str): Ticker symbol for which model was trained.
        Returns:
            ArchModel Result
        """
        
        # Create pattern for glob search
        pattern = os.path.join(model_directory, f"*{self.ticker}.pkl")
        
        # Try to find path of the latest model
        try:
            model_path = sorted(glob(pattern))[-1]
        
        # Handle possible Index Error
        except IndexError:
            raise Exception(f"No model trained for '{ticker}'.")
        
        # Load model
        self.model = joblib.load(model_path)
        