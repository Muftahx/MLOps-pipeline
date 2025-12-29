import os
import logging
import mlflow.pyfunc
import pandas as pd
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.feature_transformer import transform_raw_input

# --- Configuration ---
MODEL_NAME = "sales-quantity-classifier"
# We try Production first. If it fails, the logs will tell us.
MODEL_STAGE = "Production" 

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sales Quantity Classifier API")

# --- Model Loading Logic ---
class ModelLoader:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        """Loads the model from MLflow with Debugging."""
        print(f"🔍 DEBUG: Connecting to MLflow tracking URI...")
        try:
            # CHANGED: Used '@' instead of '/' to load by ALIAS
            model_uri = f"models:/{MODEL_NAME}@{MODEL_STAGE}"
            print(f"🔍 DEBUG: Attempting to load: {model_uri}")
            
            # Load the model
            self.model = mlflow.sklearn.load_model(model_uri)
            print("✅ DEBUG: Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ DEBUG: Failed to load model. Error details: {e}")
            self.model = None

    def predict(self, features: pd.DataFrame):
        if not self.model:
            raise RuntimeError("Model not loaded.")
        return self.model.predict(features)

# Initialize Loader
model_loader = ModelLoader()

# --- API Schemas ---
class TransactionInput(BaseModel):
    Date: str
    BranchID: str
    InvoiceNumber: str
    ItemCode: str
    QuantitySold: float
    # Optional fields to satisfy strict contracts if needed
    BranchName: Optional[str] = "Unknown"
    ItemName: Optional[str] = "Unknown"

class PredictionOutput(BaseModel):
    prediction: str
    class_id: int

# --- Endpoints ---
@app.get("/health")
def health_check():
    status = "active" if model_loader.model else "inactive"
    return {"status": status}

@app.post("/predict", response_model=PredictionOutput)
def predict_endpoint(transaction: TransactionInput):
    if not model_loader.model:
        raise HTTPException(status_code=503, detail="Model service is unavailable (Model not loaded)")
    
    try:
        # 1. Convert Input to Dict
        data_dict = transaction.dict()
        
        # 2. Transform Features (Must match training!)
        # We need to ensure the transformer uses the same logic
        features_df = transform_raw_input(data_dict)
        
        # 3. Predict
        # XGBoost returns [0, 1, 2]
        pred_idx = model_loader.predict(features_df)[0]
        
        # 4. Map to Label
        labels = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
        result_label = labels.get(int(pred_idx), "UNKNOWN")
        
        return {"prediction": result_label, "class_id": int(pred_idx)}

    except Exception as e:
        logger.error(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))