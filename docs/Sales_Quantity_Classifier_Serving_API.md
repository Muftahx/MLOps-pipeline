# Sales Quantity Classifier Serving API

This directory contains the core components for the **Serving, CI/CD & Monitoring** role within the unified MLOps project. It is responsible for deploying the trained model as a low-latency API and establishing the necessary automation and monitoring infrastructure.

## 1. Architecture Overview

The serving application is built on **FastAPI** for high-performance prediction serving and uses **MLflow** to manage the model lifecycle.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Serving API** | FastAPI, Python | Exposes the `/predict` endpoint. |
| **Model Management** | MLflow Client | Loads the model from the `Production` stage of the `sales-quantity-classifier` registry. |
| **Containerization** | Docker | Provides a portable, isolated environment for deployment via CI/CD. |
| **Monitoring** | Python/Pandas/Scipy | Scripts for detecting data drift and monitoring model health. |

## 2. Setup and Local Testing

### Prerequisites

*   Docker
*   Python 3.11+
*   Access to the MLflow Tracking Server (where the model is registered).

### 2.1. Local Environment Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the API Locally:**
    The application requires the MLflow server to be accessible. If the server is remote, set the environment variable:
    ```bash
    # Example: Set your MLflow Tracking URI
    # export MLFLOW_TRACKING_URI=http://mlflow-server:5000
    
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API documentation will be available at `http://localhost:8000/docs`.

### 2.2. Critical Integration: Feature Transformation

The `app/feature_transformer.py` module contains the feature engineering logic that transforms raw API input into the feature vector expected by the model.

**ACTION REQUIRED:** The **Data & Feature Engineer** must ensure the logic in this file is **identical** to the logic used during model training to prevent training-serving skew.

## 3. CI/CD and Deployment

The deployment process is containerized using the provided `Dockerfile`.

### 3.1. Building the Docker Image

```bash
docker build -t sales-quantity-classifier-api:latest .
```

### 3.2. CI/CD Pipeline Steps

The conceptual steps for the CI/CD pipeline are outlined in `ci_cd_script.sh`:

1.  **Test:** Run unit and integration tests.
2.  **Build:** Create the Docker image.
3.  **Tag & Push:** Tag the image with a version and push it to the container registry.
4.  **Deploy:** Update the production environment (e.g., Kubernetes, ECS) to pull the new image.

## 4. Monitoring

The `monitoring` directory contains scripts for maintaining the health of the deployed model.

### 4.1. Data Drift Monitoring

The `monitoring/data_drift_monitor.py` script compares the distribution of production features against the training baseline (`data/processed/train.csv`) using the Kolmogorov-Smirnov test.

**ACTION REQUIRED:** Ensure the baseline file `data/processed/train.csv` is accessible to the monitoring service.

### 4.2. Model Performance Monitoring

Model performance monitoring requires a system to collect ground truth data and calculate production metrics, triggering alerts or retraining flows if performance degrades.
