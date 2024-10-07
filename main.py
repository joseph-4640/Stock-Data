# Create application
from fastapi import FastAPI
import sqlite3
from data import SQLRepository
from fastapi import FastAPI
from model import GarchModel
from pydantic import BaseModel


app = FastAPI()

# "/hello" path with 200 status code
@app.get("/hello", status_code=200)
def hello():
    """Return dictionary with greetin message
    """
    
    return {"message": "Hello world!"}

# "/fit" path
# FitIn class
class FitIn(BaseModel):
    ticker: str
    use_new_data:bool
    n_observations: int
    p: int
    q: int

# FitOut Class

class FitOut(FitIn):
    success: bool
    message: str
