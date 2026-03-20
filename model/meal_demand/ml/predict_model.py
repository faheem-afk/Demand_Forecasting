from tqdm import tqdm
from ..utils.common import load_model, load_encoders, store_data, load_data, get_logger
import pandas as pd
from ..domain.config import Config
from pathlib import Path


logger = get_logger()

def predict(df):
    current_data = load_data(config=Config(file_path=Path("final_week.csv"), artifact_path=Path("../data")))
    df_future_predictions = predict_demand(current_data)

    encoders = load_encoders(config=Config(file_path=None, artifact_path=Path("../artifacts/encoders")))
    df_past = df.copy()
    df_past['period'] = 'past'
    
    df_past['meal_info'] = [item for item in df_past[['Meat', 'Other','Seafood', 'Vegetarian', 
                                    'beverage', 'dessert', 'main', 'side','starter']].values]
   
    columns = ['period','week_number','num_orders','city_id','meal_id', 'meal_info']
    df = pd.concat([df_past[columns], df_future_predictions[columns]], axis=0, ignore_index=True)
    df['current_week'] = 146
    df['meal_name'] = encoders['meal_name'].inverse_transform(df.meal_id)
    df['city_name'] = encoders['city_name'].inverse_transform(df.city_id)
    df[['meal_category', 'meal_type']] = encoders['meal_info'].inverse_transform(df['meal_info'].values.tolist())

    df.drop(columns=['city_id', 'meal_id', 'meal_info'], inplace=True)
    
    store_data(df, config=Config(file_path=Path("df_predictions.csv"), artifact_path=Path("../data")))
    logger.info("Training & Prediction Pipeline .... Completed.")
    
    return df


def predict_demand(df_week_x, future_weeks=12):
    df_week_x = df_week_x.drop(columns=['next_week_num_orders'])
    initial_week = df_week_x.week_number.max()
    city_ids = df_week_x.city_id.values
    meal_ids = df_week_x.meal_id.values
    meal_infos = df_week_x[['Meat', 'Other',
       'Seafood', 'Vegetarian', 'beverage', 'dessert', 'main', 'side',
       'starter']].values
    y_preds = []
    
    for future_week_offset in tqdm(range(1, future_weeks+1)):
        pred_week_num = initial_week + future_week_offset
        print(f"Prediction for week {pred_week_num}")
        model = load_model(f"boosted_tree_stack_week_{future_week_offset}", config=Config(file_path=None, artifact_path=Path("../artifacts/models")))
        y_pred = model.predict(df_week_x)
        y_preds.extend([{
            "period": "Future",
            "week_number": pred_week_num,
            "num_orders": y,
            "city_id": city_id,
            "meal_id": meal_id,
            "meal_info": meal_info
        } for y, city_id, meal_id, meal_info in zip(y_pred, city_ids, meal_ids, meal_infos)])

    df_preds = pd.DataFrame(y_preds)
    return df_preds



