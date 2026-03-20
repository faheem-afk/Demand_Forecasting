import logging
import re
from ..domain.config import Config
from pickle import dump, load
import pandas as pd
from pathlib import Path
import json



def get_logger():
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s; %(levelname)s; %(message)s",
        
    )
    
    logger = logging.getLogger(Path().resolve().parent.parent.name)
    
    return logger

logger = get_logger() 

def load_encoders(config: Config): 
    encoders = {}
    for file_path in config.artifact_path.glob("*encoder.pkl"):
        with open(file_path, 'rb') as f:
            encoders[re.findall(r"(.*)_encoder", file_path.name)[0]] = load(f)
    return encoders



def store_encoders(encoders, config: Config):
    (config.artifact_path).mkdir(exist_ok=True, parents=True)
    for name, obj in encoders.items():
        with open(config.artifact_path / f"{name}_encoder.pkl", 'wb') as f:
            dump(obj, f)


def load_data(config: Config) -> pd.DataFrame: 
    full_path = config.artifact_path / config.file_path
    df_train_raw = pd.read_csv(full_path)
    logger.info(f"Loaded data : path = {full_path}; len= {len(df_train_raw)}")
    return df_train_raw


def store_data(df, config: Config):
    df.to_csv(config.artifact_path /  config.file_path, index=False)
    logger.info("Storing data ... Successful.")
    

def store_model(model_name, model, config: Config):
    full_path = config.artifact_path
    full_path.mkdir(exist_ok=True, parents=True)
    with open(full_path / f"{model_name}.pkl", 'wb') as f:
        dump(model, f) 

def load_model(model_name, config: Config):
    full_path = config.artifact_path
    with open(full_path / f"{model_name}.pkl", 'rb') as f:
        m = load(f) 
    return m

def store_bestParams(params, config: Config):
    full_path = config.artifact_path
    full_path.mkdir(exist_ok=True, parents=True)
    with open(full_path / config.file_path, 'w') as f:
        json.dump(params, f)

