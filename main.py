# Create application
from fastapi import FastAPI

app = FastAPI()

# "/hello" path with 200 status code
@app.get("/hello", status_code=200)
def hello():
    """Return dictionary with greetin message
    """
    
    return {"message": "Hello world!"}