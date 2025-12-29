import pandas as pd
import numpy as np
from typing import Dict, Any
from src.utils import stable_hash_to_bucket, add_date_features

# Must match the buckets used in feature_engineering.py
BUCKETS = {
    "item": 2000,
    "branch": 200,
    "invoice": 5000,
    "item_branch": 5000,
    "item_month": 5000
}

def transform_raw_input(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Transforms a single transaction dictionary into a DataFrame 
    with EXACTLY the features expected by the XGBoost model.
    """
    
    # 1. Create Initial DataFrame
    df = pd.DataFrame([data])
    
    # 2. Date Features
    df = add_date_features(df, date_col="Date")
    
    # 3. Hashing Features (Recreating logic from feature_engineering.py)
    df["h_item"] = df["ItemCode"].astype(str).apply(lambda x: stable_hash_to_bucket(x, BUCKETS["item"]))
    df["h_branch"] = df["BranchID"].astype(str).apply(lambda x: stable_hash_to_bucket(x, BUCKETS["branch"]))
    df["h_invoice"] = df["InvoiceNumber"].astype(str).apply(lambda x: stable_hash_to_bucket(x, BUCKETS["invoice"]))
    
    # Cross Features
    df["h_item_branch"] = (df["ItemCode"] + df["BranchID"]).apply(lambda x: stable_hash_to_bucket(x, BUCKETS["item_branch"]))
    df["h_item_month"] = (df["ItemCode"] + df["month"].astype(str)).apply(lambda x: stable_hash_to_bucket(x, BUCKETS["item_month"]))
    
    # 4. Fill Time-Series Features with Default/Zero
    # The model expects these lags, but for a single API call, we don't have history.
    # We fill them with 0.0 to match the schema.
    ts_features = [
        'qty_lag_1', 'qty_lag_2', 'qty_lag_3', 'qty_lag_7', 'qty_lag_14',
        'qty_roll_mean_3', 'qty_roll_std_3', 
        'qty_roll_mean_7', 'qty_roll_std_7', 
        'qty_roll_mean_14', 'qty_roll_std_14', 
        'qty_roll_mean_30', 'qty_roll_std_30'
    ]
    
    for col in ts_features:
        df[col] = 0.0
        
    # 5. Select & Order Columns Exactly as Model Expects
    expected_cols = [
        'year', 'month', 'day', 'dayofweek', 'is_weekend', 
        'h_item', 'h_branch', 'h_invoice', 'h_item_branch', 'h_item_month'
    ] + ts_features
    
    # Ensure purely numeric types for XGBoost
    df_final = df[expected_cols].astype(float)
    
    return df_final