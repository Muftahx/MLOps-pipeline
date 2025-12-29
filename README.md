````md
# 📈 Sales Quantity Classifier (MLOps Pipeline)

An end-to-end MLOps project that automates data processing, model training, tracking, and deployment. This system predicts sales quantity categories (e.g., `LOW`, `HIGH`) based on transaction data.

---

## 🚀 Key Features

- **Automated Pipeline:** Orchestrated using **Prefect** to handle Feature Engineering, Training, and Evaluation.
- **Model Registry:** Uses **MLflow** to track experiments, metrics, and manage model versions.
- **Real-time Serving:** Deploys the model as a REST API using **FastAPI**.
- **Containerization:** Fully Dockerized application with auto-training capabilities.
- **Robust Testing:** Includes automated health checks and integration tests.

---

## 📂 Project Structure

```text
MLops2.0-main/
├── configs/             # Configuration files for features and model parameters
├── data/                # Raw and processed datasets
├── pipelines/           # Prefect flows (Orchestration logic)
├── src/                 # Source code (Training, Feature Eng., API)
├── tests/               # Integration checks for the API
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
├── validate_pipeline.py # System health check script
└── README.md            # Project documentation
````

---

## 🐳 Quick Start (Docker)

### 1️⃣ Build the Image

We use `--no-cache` to ensure the model trains using the latest code and data.

```bash
docker build --no-cache -t sales-classifier:v1 .
```

### 2️⃣ Run the Container

Starts the FastAPI server on port `8000`.

```bash
docker run -p 8000:8000 sales-classifier:v1
```

---

## ✅ Validation & Testing

This project includes tools to verify the integrity of the pipeline and API before deployment.

### 🩺 Pipeline Validator (`validate_pipeline.py`)

Runs a full **system health check**, validating:

* Required project files and directories
* Processed dataset schema
* Presence of a trained and registered MLflow model

```bash
python validate_pipeline.py
```

**Expected Output:**

```text
✅ PASSED: All checks passed successfully!
```

---

### 🧪 Automated Tests (`tests/`)

Uses **pytest** to run integration tests on the API logic, ensuring the prediction endpoint behaves correctly.

```bash
python -m pytest tests/
```

**Expected Output:**

```text
===== 2 passed in 1.05s =====
```

---

## ⚡ API Usage

### 🔁 Using CURL (Terminal)

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "Date": "2025-04-26",
           "BranchID": "7",
           "InvoiceNumber": "INV-TEST",
           "ItemCode": "58842",
           "QuantitySold": 1
         }'
```

**Expected Response:**

```json
{
  "prediction": "LOW",
  "class_id": 0
}
```

---

## 🔧 Troubleshooting

### ❗ Model Not Found / Path Errors

* The model is **trained inside the Docker image during build time**
* Do **NOT** mount a Windows-created `mlflow.db` into the container
* Always rebuild with:

```bash
docker build --no-cache -t sales-classifier:v1 .
```

