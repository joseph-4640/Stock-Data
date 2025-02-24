
# Stock Data Project

This project is designed to interact with the Alpha Vantage API, test various functionalities, and deploy machine learning models using FastAPI. It comprises several Jupyter notebooks and Python scripts to facilitate API access, testing, and deployment of a GARCH model.


# Project Structure

```
Stock-Data/
├── APIs.ipynb
├── Testing.ipynb
├── data.py
├── main.py
├── model.py
└── deploy.ipynb
```

# Requirements

Make sure you have the following packages installed:

- FastAPI
- uvicorn
- requests
- pandas
- sqllite
- jupyter
- statsmodels (for GARCH model)
- pandas


# Files

1. **APIs.ipynb**: 
   - This notebook provides functionality for accessing the Alpha Vantage API. It contains code to fetch stock data and handle API responses.

2. **Testing.ipynb**: 
   - This notebook is used for testing the functionality of the Alpha Vantage API class and SQL repository class. It includes various test cases to ensure the correctness of the implementation.

3. **data.py**: 
   - Contains the code for building the Alpha Vantage API class and the SQL repository class. This file handles data retrieval and storage functionalities.

4. **main.py**: 
   - This script contains the backend code for the FastAPI application. It sets up the web server and defines the API endpoints for interacting with the stock data.

5. **model.py**: 
   - Implements the GARCH model class, which is used for time series forecasting and volatility modeling.

6. **deploy.ipynb**: 
   - This notebook contains the code for building and deploying the GARCH model. It provides steps for model training and saving the model for later use.

## Usage

To run the FastAPI application, execute the following command in your terminal:

```bash
uvicorn main:app --reload
```

This command will start the FastAPI server, and you can access the API at `http://127.0.0.1:8080`.

Use the **APIs.ipynb** and **Testing.ipynb** notebooks to explore and test the functionalities of the API.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
```
