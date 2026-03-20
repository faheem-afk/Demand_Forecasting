from meal_demand.ml.predict_model import predict
from meal_demand.visualization.visuals import show_visuals
from meal_demand.utils.common import load_data
from meal_demand.domain.config import Config
from pathlib import Path
from postgres import upload_to_postgres

def generate_forecast():
    df = load_data(config=Config(file_path=Path("df_encoded.csv"), artifact_path=Path("../data")))
    df = predict(df)
    show_visuals(df)
    upload_to_postgres(df, "current_meal_demand")
