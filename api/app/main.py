from pydantic import BaseModel
import os
from postgres import run_postgres_query
from fastapi import FastAPI, HTTPException
from datetime import datetime

db_args = dict(
    host = os.getenv("POSTGRES_HOST"),
    user = os.getenv("POSTGRES_USER"),
    dbname = os.getenv("POSTGRES_DB"),
    port = os.getenv("POSTGRES_PORT")
)


app = FastAPI()


class ForecastRequest(BaseModel):
    city_name: str
    meal_name: str
    
@app.post("/forecast")
def fetch_forecast(request: ForecastRequest):
    try:
        query = f""" 
                SELECT *
                FROM current_meal_demand
                WHERE 
                    city_name = %s
                    and meal_name = %s
            
            """
        params = (request.city_name, request.meal_name)
        forecast_df = run_postgres_query(
            query,
            params,
            **db_args
        )
        
        forecast_df = forecast_df.to_dict(orient="records")
        return {
            "request": {"city_name": request.city_name, "meal_name": request.meal_name, "data": datetime.now().isoformat()},
            "result": forecast_df
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
             