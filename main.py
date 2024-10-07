# Create application
from fastapi import FastAPI
import sqlite3
from data import SQLRepository
from fastapi import FastAPI
from model import GarchModel
from pydantic import BaseModel

<<<<<<< HEAD
=======

>>>>>>> d5415fc0024b9e49d5ae3606013c9a93a404d87a
app = FastAPI()

# "/hello" path with 200 status code
@app.get("/hello", status_code=200)
def hello():
    """Return dictionary with greetin message
    """
    
<<<<<<< HEAD
    return {"message": "Hello world!"}
=======
    return {"message": "Hello world!"}

# "/fit" path
# FitIn class
class FitIn(BaseModel):
    ticker:str
    use_new_data:bool
    n_observations: int
    p:int
    q:int

# FitOut Class

class FitOut(FitIn):
    success: bool
    message: str
>>>>>>> d5415fc0024b9e49d5ae3606013c9a93a404d87a
