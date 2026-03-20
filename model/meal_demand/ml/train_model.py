from tqdm import tqdm
from pathlib import Path
from ..utils.common import store_model, get_logger
from ..domain.config import Config


logger = get_logger()

def train(model, df, fit):
    
    if fit:
        config = Config(file_path = None, artifact_path = Path("../artifacts/models"))
        num_future_weeks = 12
    

        for future_week_num in tqdm(list(range(1, num_future_weeks+1))):
            if future_week_num == 1:
                df_i = df.rename(columns={"next_week_num_orders": "target_num_orders"}).copy()
            else:
                df_i["target_num_orders"] = df_i.groupby(['city_id', 'meal_id']).target_num_orders.shift(-1)
                df_i = df_i.dropna().copy()

            logger.info(f"week_num={future_week_num}")
            logger.info(f"len(df)={int(len(df_i))}")
            logger.info(f"max_week={int(df_i.week_number.max())}")

            X = df_i.drop(columns = ['target_num_orders'])
            y = df_i['target_num_orders']

            model.fit(X, y)

            store_model(f"boosted_tree_stack_week_{future_week_num}", model, config)
            

            
                