from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from ..utils.common import store_model, store_bestParams
from ..domain.config import Config
from pathlib import Path

def Tuning(df, fit):

    if fit:
        
        param_config = Config(file_path="bestParams.json", artifact_path = Path("../artifacts/tuned-params"))
        model_config = Config(file_path=None, artifact_path = Path("../artifacts/tuned-model"))
        
        X = df.drop(columns=['next_week_num_orders'])
        y = df['next_week_num_orders']

        tscv = TimeSeriesSplit(n_splits=3, test_size=12)

        model = XGBRegressor(
            objective="reg:squarederror",
            random_state=42,
            n_jobs=-1
        )

        param_grid = {
            "n_estimators": [100, 200, 300],
            "learning_rate": [0.01, 0.05, 0.1],
            "max_depth": [3, 4, 5],
            "subsample": [0.8, 0.9, 1.0],
            "colsample_bytree": [0.8, 1.0],
            "min_child_weight": [1, 3]
        }

        grid_search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=tscv,
            scoring="neg_mean_squared_error",
            n_jobs=-1,
            verbose=2
        )


        grid_search.fit(X, y)
        
        model = grid_search.best_estimator_ 
        params = grid_search.best_params_ 
        
        store_model("Xgboost", model, model_config)
        store_bestParams(params, param_config)
        
        return model