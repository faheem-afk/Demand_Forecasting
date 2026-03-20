from sklearn.preprocessing import StandardScaler
from ..domain.config import Config
from ..utils.common import *


logger = get_logger()

    
def feat_scale(df, fit=False):
    config = Config(file_path=None, artifact_path=Path('../artifacts/encoders'))
    if fit:
        encoder = {}
        encoder["price_scaler"] = StandardScaler()
    else:
        encoder = load_encoders()
     
    df, encoder = apply_scaling(df, encoder, fit)
    
    if fit: 
        store_encoders(encoder, config)
    
    store_data(df, config=Config(file_path=Path("df_scaled.csv"), artifact_path=Path("../data")))
    
    return df
    

def apply_scaling(df, encoder, fit):
    if fit:
        df[['base_price', 'checkout_price']] = encoder["price_scaler"].fit_transform(df[['base_price', 'checkout_price']])
    else:
         df[['base_price', 'checkout_price']] = encoder["price_scaler"].transform(df[['base_price', 'checkout_price']])
    logger.info("Applying Scaling ... Successfull.")
    return df, encoder


