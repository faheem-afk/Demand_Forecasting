import numpy as np
from ..utils.common import get_logger, store_data
from ..domain.config import Config
from pathlib import Path

logger = get_logger()

def add_features(df):
    df = _add_price_feature(df)
    df = _add_calendar_features(df)
    df, df_final_week = _add_rolling_features(df)
    config = Config(file_path = Path("final_week.csv"), artifact_path = Path("../data"))
    store_data(df_final_week, config)
    
    logger.info("Adding Calender & Temporal features .... Successful.")
    
    store_data(df, config=Config(file_path=Path("df_temporal_features.csv"), artifact_path=Path("../data")))
    return df
    

def _add_calendar_features(df):
    df['year_num'] = (df.week_number // 52 + 1).astype(int)
    df['month_num'] = (df.week_number // (52/12) + 1).astype(int).apply(_apply_yearly_offset_by_month)
    df['quarter_num'] = (df.week_number // (52/4) + 1).astype(int).apply(_apply_yearly_offset_by_quarter)
    df['week_of_year'] = (df.week_number - 1) % 52 + 1
    df["week_sin"] = np.sin(2 * np.pi * df["week_of_year"] / 52)
    df["week_cos"] = np.cos(2 * np.pi * df["week_of_year"] / 52)
    return df


def _add_rolling_features(df):
    df = df.sort_values("week_number", ascending=True).copy()

    g = ['city_id', 'meal_id']

    df['next_week_num_orders'] = df.groupby(g).num_orders.shift(-1).fillna(0)

    df['num_orders_last_year'] = df.groupby(g).next_week_num_orders.shift(52).fillna(0)

    df['num_orders_last_week'] = df.groupby(g).num_orders.shift(1).fillna(0)

    df['num_orders_rolling_4_week'] = df.groupby(g).num_orders.rolling(4).mean() \
                        .reset_index().sort_values('level_2').drop(columns=g).set_index('level_2').num_orders.fillna(0)

    df['num_orders_rolling_16_week'] = df.groupby(g).num_orders.rolling(16).mean() \
                        .reset_index().sort_values('level_2').drop(columns=g).set_index('level_2').num_orders.fillna(0)

    df['num_orders_last_year_rolling_4_weeks'] = df.groupby(g).num_orders_rolling_4_week.shift(52).fillna(0)
    
    df['num_orders_last_year_rolling_16_weeks'] = df.groupby(g).num_orders_rolling_16_week.shift(52).fillna(0)

    df_final_week = df[df.week_number == 145].copy()

    df = df[(df.week_number > 52) & (df.week_number != 145) ]
    
    store_data(df, config=Config(file_path=Path("processed_df.csv"), artifact_path=Path("../data")))

    return df, df_final_week




def _add_price_feature(df):
    df['price_diff'] = df.base_price - df.checkout_price
    return df
    
    
def _apply_yearly_offset_by_month(month_num):
    if month_num <= 12:
        return month_num
    elif month_num <= 24:
        return month_num - 12
    elif month_num <= 36:
        return month_num - 24

        
    
def _apply_yearly_offset_by_quarter(quater_num):
    if quater_num <= 4:
        return quater_num
    elif quater_num <= 8:
        return quater_num - 4
    elif quater_num <= 12:
        return quater_num - 8
    


