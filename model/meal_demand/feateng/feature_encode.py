from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pandas as pd
import numpy as np
from ..domain.config import Config
from ..utils.common import *
from meal_demand.feateng.customEncoder import OrderedCategoryEncoder

logger = get_logger()

    
def feat_encode(df, fit=False):
    config = Config(file_path=None, artifact_path=Path('../artifacts/encoders'))
    if fit:
        encoders = {}
        encoders["meal_info"] = OneHotEncoder()
        encoders["city_name"] = OrderedCategoryEncoder()
        encoders["meal_name"] = OrderedCategoryEncoder()

    else:
        encoders = load_encoders()
        
    df, encoders = encode_features(df, encoders, fit)    
    
    if fit: 
        store_encoders(encoders, config)
    
    return df
        

def encode_features(df, encoders, fit):
 
    df = apply_ohe_encoding(df, encoders['meal_info'], fit)
    df = apply_ordinal_encoding(df, encoders['city_name'], encoders['meal_name'], fit)
    logger.info("Done encoding dataset")
    logger.info("------------------------------------------------------")
        
    return df, encoders

def get_ohe_columns(ohe_encoder):
    columns = []
    for cols in ohe_encoder.categories_:
        columns.extend(list(cols))
    return columns


def apply_ohe_encoding(df, meal_info_ohe, fit):
    logger.info("Applying one-hot-encoding to meal_category and meal_type")
    if fit:
        ohe_vals = meal_info_ohe.fit_transform(df[["meal_category", "meal_type"]].values)
    else:
        ohe_vals = meal_info_ohe.transform(df[["meal_category", "meal_type"]].values)
        
    df_ohe = pd.DataFrame(ohe_vals.toarray(), columns=get_ohe_columns(meal_info_ohe)).astype(int)
    df = pd.concat((df.reset_index(drop=True), df_ohe.reset_index(drop=True)), axis=1)
    df.drop(columns=['meal_category', 'meal_type'], inplace=True)
    return df


def apply_ordinal_encoding(df, city_name_encoder, meal_name_encoder, fit):
    
    if fit:
        logger.info('Applying ordered categorical encoding to city_name')
        ordered_city_names = df.groupby('city_name')['num_orders'].sum().sort_values().reset_index().city_name.tolist()
        logger.info('Applying ordered categorical encoding to city_name')
        city_name_encoder.fit(ordered_city_names)
        df['city_id'] = city_name_encoder.transform(df.city_name.values)
        
        logger.info('Applying ordered categorical encoding to meal_name')
        ordered_meal_name = df.groupby('meal_name').num_orders.sum().sort_values().reset_index().meal_name.tolist()
        meal_name_encoder.fit(ordered_meal_name)
        df['meal_id'] = meal_name_encoder.transform(df.meal_name.values)
    else:
        logger.info('Applying ordered categorical encoding to city_name')
        df['city_id'] = city_name_encoder.transform(df.city_name.values)
        
        logger.info('Applying ordered categorical encoding to meal_name')
        df['meal_id'] = meal_name_encoder.transform(df.meal_name.values)

    
    df = df.drop(columns = ['city_name', 'meal_name'])
    
    store_data(df, config=Config(file_path=Path("df_encoded.csv"), artifact_path=Path("../data")))

    return df
            

