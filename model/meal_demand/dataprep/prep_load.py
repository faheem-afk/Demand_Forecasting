from ..domain.config import  Config
from ..utils.common import *


logger = get_logger()

def data_ingestion():
    """
    Loads data for prediction or training.
    """
    logger.info("Started dataprep: step=load")
    config = Config(file_path=Path("meal_demand_historical.csv"), artifact_path=Path("../data"))
    df = load_data(config)
    logger.info("Completed dataprep: step=load")
    return df


