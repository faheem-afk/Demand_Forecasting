import os
from meal_demand.ml.predict_model import predict
from meal_demand.visualization.visuals import show_visuals
from meal_demand.utils.common import load_data
from meal_demand.domain.config import Config
from pathlib import Path
from postgres import upload_to_postgres, run_query


db_args = dict(
    host = os.getenv("POSTGRES_HOST"),
    user = os.getenv("POSTGRES_USER"),
    dbname = os.getenv("POSTGRES_DB"),
    port = os.getenv("POSTGRES_PORT")
)

def generate_forecast():
    table_name = db_args.get("host")
    df = load_data(config=Config(file_path=Path("df_encoded.csv"), artifact_path=Path("../data")))
    df = predict(df)
    show_visuals(df)
    run_query(
        f"""DROP TABLE IF EXISTS {table_name}""",fetch=False, **db_args
    )
    upload_to_postgres(df, table_name, **db_args)
