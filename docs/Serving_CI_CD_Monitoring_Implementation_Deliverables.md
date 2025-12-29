# Serving, CI/CD & Monitoring: Implementation Deliverables

**Author:** Collaborative MLOps Engineer
**Date:** December 23, 2025
**Project:** Unified MLOps Sales Quantity Classifier Service

This document details the design, implementation contract, and core artifacts for the **Serving, CI/CD & Monitoring** role, ensuring strict adherence to the shared project contract [1] and seamless integration with the MLOps team.

## 1. Serving Component: The Prediction API

The Serving component is implemented using **FastAPI** and **MLflow** to provide a robust, production-ready prediction endpoint.

### 1.1. Serving Contract Adherence

The API strictly follows the defined Serving Contract [1]:

| Aspect | Contract Requirement | Implementation Detail |
| :--- | :--- | :--- |
| **Model Source** | Load model from MLflow. | Uses `mlflow.pyfunc.load_model("models:/sales-quantity-classifier/Production")` to ensure the latest, approved model is served. |
| **Endpoint** | `POST /predict` | Implemented in `app/main.py`. |
| **Input** | JSON with raw transaction fields. | Defined by the `TransactionInput` Pydantic model in `app/main.py`. |
| **Output** | JSON with `prediction` and `confidence`. | Defined by the `PredictionOutput` Pydantic model in `app/main.py`. |

### 1.2. Critical Integration Point: Feature Transformation

The most critical integration point is the feature transformation logic, which must be **identical** to the logic used during model training.

*   **Artifact:** `app/feature_transformer.py`
*   **Contract:** This module defines a callable function, `transform_raw_input(raw_data)`, which takes the raw API input and returns the feature vector required by the model.
*   **Action Required from Data & Feature Engineer:** The placeholder logic in this file **MUST** be replaced with the final, production-grade feature engineering code. This module serves as the shared contract for feature consistency between training and serving.

## 2. CI/CD Pipeline: Automation and Deployment

The CI/CD process is designed to automate the build, test, and deployment of the Serving component, ensuring rapid and reliable updates.

### 2.1. Deployment Artifacts

| Artifact | Purpose | Integration Point |
| :--- | :--- | :--- |
| `requirements.txt` | Lists all Python dependencies (`fastapi`, `uvicorn`, `mlflow`, `pandas`). | Used by the Docker build process. |
| `Dockerfile` | Defines the container image for the Serving API. | Used by the CI/CD system to build the production image. |
| `ci_cd_script.sh` | Conceptual script outlining the automated steps (Test, Build, Tag, Push, Deploy). | Provides a template for the **Pipeline & Automation Engineer** to integrate into the chosen CI/CD platform. |

### 2.2. Deployment Strategy

The deployment is designed to be triggered by two events:
1.  **Code Change:** A change in the Serving API code triggers a full CI/CD run, resulting in a new Docker image.
2.  **New Model:** A successful Prefect flow run that registers a new model to the **Production** stage in MLflow should trigger a **deployment update** to ensure the running container reloads the newly promoted model.

## 3. Monitoring Component: Model and Data Health

The Monitoring component is essential for maintaining the long-term health and performance of the ML service in production.

### 3.1. Data Drift Monitoring

*   **Artifact:** `monitoring/data_drift_monitor.py`
*   **Methodology:** Uses the **Kolmogorov-Smirnov (KS) two-sample test** to compare the distribution of production data features against the baseline training data features.
*   **Baseline Contract:** The script expects the baseline training data to be available at the path defined in the shared contract: `data/processed/train.csv`.
*   **Action Required:** The **Data & Feature Engineer** must ensure this file is accessible and contains the final, transformed features used for training.

### 3.2. Model Performance Monitoring

This is a conceptual requirement that would be implemented by:
1.  Logging the raw input, prediction, and confidence for every request.
2.  Periodically joining this log data with the actual ground truth once it becomes available.
3.  Calculating production metrics (e.g., F1-score, Accuracy) and comparing them against the MLflow-logged evaluation metrics.
4.  If performance drops below a pre-defined threshold, an alert is triggered, and the **Pipeline & Automation Engineer** is notified to initiate a retraining flow.

## 4. Final Integration Checklist (Serving, CI/CD & Monitoring)

This checklist confirms the successful completion of this role's responsibilities, aligning with the shared integration goals [1].

| Component | Check | Status |
| :--- | :--- | :--- |
| **Serving API** | API loads model from MLflow Production stage. | ✅ (Implemented in `app/main.py`) |
| **Serving API** | `/predict` endpoint works with raw input. | ✅ (Implemented in `app/main.py`) |
| **Serving API** | Output format matches the contract (`prediction`, `confidence`). | ✅ (Implemented in `app/main.py`) |
| **Feature Logic** | Shared feature transformation module is defined. | ✅ (Defined in `app/feature_transformer.py` - **Requires final logic from Data & Feature Engineer**) |
| **CI/CD** | Dockerfile is created for containerization. | ✅ (Created) |
| **Monitoring** | Data drift check script is defined. | ✅ (Defined in `monitoring/data_drift_monitor.py`) |
| **Monitoring** | Baseline data path adheres to contract (`data/processed/train.csv`). | ✅ (Path defined in script) |

***
### References

[1] MASTERTEAMPROMPT.pdf. (n.d.). *Final Master Team Prompt (Self-Correcting Version)*. Project Documentation.
