# MLflow Experiment Tracking – Sales Quantity Classifier

This project demonstrates basic MLflow experiment tracking and model registry usage.

## Overview
- A Logistic Regression model is trained using the sklearn breast cancer dataset.
- Parameters, metrics, and the trained model are logged to MLflow.
- The model is registered in the MLflow Model Registry.
- The registered model version is assigned the **@production** alias.

## Experiment Details
- Experiment name: `sales-quantity-experiment`
- Model: Logistic Regression
- Parameters:
  - model_type: LogisticRegression
  - max_iter: 1000
- Metric:
  - accuracy ≈ 0.835

## Files
- `mlflow_experiment.py` – MLflow experiment and model registration script
- `Screenshots/` – MLflow UI screenshots (experiments, run details, registry, production alias)
- `Mlflow_Report.md` – Short report describing the experiment
- `requirements.txt` – Required Python dependencies

## How to Run (Optional)
```bash
pip install -r requirements.txt
mlflow ui
python mlflow_experiment.py
```
