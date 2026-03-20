from ..domain.config import  Config
import pandas as pd 
from ..utils.common import *
from tqdm import tqdm


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = _parse_num_orders(df)
    df = _clean_num_orders(df)
    df = _remove_low_temporal_coverage(df)
    logger.info("Done cleaning dataset")
    logger.info("-------------------------------------------------------------")

    store_data(df, config=Config(file_path=Path("df_preprocessed.csv"), artifact_path=Path("../data")))
    return df

def _parse_num_orders(df):
    logger.info(f"Length before parsing num_orders: {len(df)}")
    nulls = df['num_orders'].isnull()
    df = df[~nulls].copy() # this is a business decision as we don't normally do this without consulting the client.
    # instead of just dropping them, we could have performed forward filling for that specific city, meal category or meal type.
    df['num_orders']= df['num_orders'].str.replace(",", "")
    df['num_orders'] = pd.to_numeric(df['num_orders'])
    logger.info(f"Length after parsing num_orders: {len(df)}")
    return df

def _clean_num_orders(df):
    logger.info(f"Length before cleaning num_orders: {len(df)}")
    max_value = 6.902760e+03
    negative_orders = df['num_orders'] < 0
    zero_orders = df['num_orders'] == 0 
    huge_orders = df['num_orders'] > max_value
    df = df[~(negative_orders | zero_orders | huge_orders)].copy()
    logger.info(f"Length after cleaning num_orders: {len(df)}")
    return df

def _remove_low_temporal_coverage(df): 
    logger.info(f"Length before removing low temporal coverage records: {len(df)}")
    df = df[~(df['city_name'] == 'Osprey Point')].copy()

    temporal_agg = df.groupby(['city_name', 'meal_name']).agg({'week_number': [len, 'min', 'max']})['week_number']
    temporal_agg['week_range'] = temporal_agg['max'] - temporal_agg['min'] + 1
    temporal_agg['temporal_issue'] = temporal_agg['len'] != temporal_agg['week_range']

    city_meal_dfs = []
    for _, record in tqdm(df[['city_name', 'meal_name']].drop_duplicates().sort_values(['city_name', 'meal_name']).iterrows(), total=3547):
    
        df_city_meal = df[(df.city_name == record.city_name) & (df.meal_name == record.meal_name)].copy()
        df_missing_weeks = pd.DataFrame(list(range(df_city_meal.week_number.min(), df_city_meal.week_number.max()+1)), columns=['week_number'])
        
        df_city_meal = pd.merge(
            df_city_meal,
            df_missing_weeks,
            on='week_number',
            how='outer'
        )
    
        df_city_meal['num_orders'] = df_city_meal.num_orders.fillna(0)
        df_city_meal = df_city_meal.sort_values("week_number")
        df_city_meal = df_city_meal.ffill()
        city_meal_dfs.append(df_city_meal)

    df = pd.concat(city_meal_dfs)

    logger.info(f"Length after removing low temporal coverage records: {len(df)}")
    return df
    

