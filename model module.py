import pandas as pd
from data import SQLRepository
from data import AlphaVantageAPI
from arch import arch_model
import sqlite3
from settings import model_directory


class GarchModel:
    """ Garch model class with methods for wrangling data, training, predicting, serving and loading models.
    """
    
    def __init__(self, ticker, repo, use_new_data):
        self.ticker=ticker
        self.repo=repo
        self.use_new_data=use_new_data
        self.model_directory = settings.model_directory