import sqlite3
from fastapi import FastAPI
from data import SQLRepository
from model import GarchModel
from pydantic import BaseModel, validator


# Create Application
app = FastAPI()

# "/hello" path with 200 status code
@app.get("/hello", status_code=200)
def hello():
    """Return dictionary with greeting message.
    """
    
    return {"message": "Hello World!"}


# "fit in" path
# FitIn Class

class FitIn(BaseModel):
    ticker: str
    use_new_data: bool
    n_observations: int
    p: int
    q: int


# FitOut Class
class FitOut(FitIn):
<<<<<<< HEAD
    success:bool
    message:str

# Build Model Function
=======
    success: bool
    message: str


>>>>>>> e4540dd76bad35e6ce6aca067df706cc7408ed9e
def build_model(ticker, use_new_data):
    # Connect to database
    connection = sqlite3.connect("/home/denis/Stock-Data/sqlite.db", check_same_thread=False)

    # Create an isnstace of the SQLRepository class
    repo = SQLRepository(connection=connection)
    
    # Create Model
    model = GarchModel(ticker="BABA", use_new_data=use_new_data, repo=repo)
    
    return model


@app.post("/fit", status_code=200, response_model=FitOut)
def fit_model(request: FitIn):
    """Fit model, return confirmation messages.

    Args:
        request (FitIn)
    Returns:
        dict: Must conform to FitOut class
    """
    
    # Create dictionary from payload
    response = request.dict()
    
    # Create try block to handle exceptions
    try:
        # Build model with "build model function"
        model = build_model(ticker=request.ticker, use_new_data=request.use_new_data)
        
        # Wrangle data
        model.wrangle_data(n_observations=request.n_observations)
        
        # Fit model
        model.fit(p=request.p, q=request.q)
        
        # Save model
        filename = model.dump()
        
        # Add "success" key to "response"
        response["success"] = True
        
        # Add message key to response with filename
        response["message"] = f"Trained and Saved{filename}"
    
    # Create except block
    except Exception as e:
        # Add 'success' key to 'response'
        response["success"] = False
        
        # Add 'message' key to 'reponse' with error message
        response["message"] = str(e)
    
    return response


# "/Predict" Path
# PredictIn Class
class PredictIn(BaseModel):
    ticker:str
    n_days:int

# PredictOut Class
class PredictOut(PredictIn):
    success:bool
    forecast:dict
    message:str 


# "Predict" path: build path
@app.post("/predict", status_code=200, response_model=PredictOut)
def get_prediction(request: PredictIn):
    # Create dictionary from request
    response = request.dict()
    
    # Create try block to handle exceptions
    try:
        # Build model with 'build model' function
        model = build.model(ticker=request.ticker)
        
        # Load Stored model
        model.load()
        
        # Generate Prediction
        prediction = model.predict_volatility(horizon=request.n_days) 
        
        # Add 'success' key to response
        response["success"] = True
        
        # Add 'forecast' key to response
        response["forecast"] = prediction
        
        # Add 'message' key to response
        response["message"] = f"{request.n_days} days prediction"
    
    # Create except block
    except Exception as e:
        # Add 'success' key to response
        response["success"] = False
        
        # Add forecast key to response
        response["forecast"] = {}
        
        # Add 'message' key to response
        response["message"] = str(e)

=======
<<<<<<< HEAD
    model = GarchModel(ticker="BABA", use_new_data=use_new_data, repo=repo)
    
    return model


@app.post("/fit", status_code=200, response_model=FitOut)
def fit_model(request: FitIn):
    """Fit model, return confirmation messages.

    Args:
        request (FitIn)
    Returns:
        dict: Must conform to FitOut class
    """
    
    # Create dictionary from payload
    response = request.dict()
    
    # Create try block to handle exceptions
    try:
        # Build model with "build model function"
        model = build_model(ticker=request.ticker, use_new_data=request.use_new_data)
        
        # Wrangle data
        model.wrangle_data(n_observations=request.n_observations)
        
        # Fit model
        model.fit(p=request.p, q=request.q)
        
        # Save model
        filename = model.dump()
        
        # Add "success" key to "response"
        response["success"] = True
        
        # Add message key to response with filename
        response["message"] = f"Trained and Saved{filename}"
    
    # Create except block
    except Exception as e:
        # Add 'success' key to 'response'
        response["success"] = False
        
        # Add 'message' key to 'reponse' with error message
        response["message"] = str(e)
    
    return response


# "/Predict" Path
# PredictIn Class
class PredictIn(BaseModel):
    ticker:str
    n_days:int

# PredictOut Class
class PredictOut(PredictIn):
    success:bool
    forecast:dict
    message:str 
    
    @validator('message', pre=True, always=True)
    def ensure_message_is_string(cls, v):
        if not isinstance(v, str):
            raise ValueError('message must be a string')
        return v



# "Predict" path: build path
@app.post("/predict", status_code=200, response_model=PredictOut)
def get_prediction(request: PredictIn):
    # Create dictionary from request
    response = request.dict()
    
    # Create try block to handle exceptions
    try:
        # Build model with 'build model' function
        model = build.model(ticker=request.ticker)
        
        # Load Stored model
        model.load()
        
        # Generate Prediction
        prediction = model.predict_volatility(horizon=request.n_days) 
        
        # Add 'success' key to response
        response["success"] = True
        
        # Add 'forecast' key to response
        response["forecast"] = prediction
        
        # Add 'message' key to response
        response["message"] = f"{request.n_days} days prediction"
    
    # Create except block
    except Exception as e:
        # Add 'success' key to response
        response["success"] = False
        
        # Add forecast key to response
        response["forecast"] = {}
        
        # Add 'message' key to response
        response["message"] = "Error occured while processing the prediction stage"

=======
    model = GarchModel(ticker=ticker, use_new_data=True, repo=repo)
    
    return model
>>>>>>> e4540dd76bad35e6ce6aca067df706cc7408ed9e
