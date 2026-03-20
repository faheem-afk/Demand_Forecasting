from meal_demand.dataprep.prep_load import data_ingestion
from meal_demand.dataprep.preprocessing import preprocess
from meal_demand.feateng.feature_encode import feat_encode 
from meal_demand.feateng.feature_scaling import feat_scale
from meal_demand.feateng.feat_ts import add_features
from meal_demand.ml.hyperparameterTuning import Tuning
from meal_demand.ml.train_model import train
from meal_demand.utils.common import  get_logger





logger = get_logger()

def train_models():
    df = data_ingestion()
    df = preprocess(df)
    df = feat_encode(df, True)
    df = feat_scale(df, True)
    df = add_features(df)
    model = Tuning(df, True)
    train(model, df, True)
  
    
    
    
    
    
