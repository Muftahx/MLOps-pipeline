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

## 🛠️ Manual Installation (Run Without Docker)

If you prefer to run the project locally on your machine, follow these steps.

### 1️⃣ Set Up Environment

Create and activate a virtual environment.

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Run the Training Pipeline

Execute the Prefect flow to clean data, train the model, and register it in MLflow.

```bash
python -m pipelines.prefect_flow
```

This creates a local `mlruns/` directory and `mlflow.db`.

---

### 3️⃣ Start the API Server

Launch the FastAPI application.

```bash
uvicorn src.serve_api:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ Validation & Testing

Tools are provided to verify pipeline and API correctness.

### 🩺 Pipeline Validator

Runs a full system health check.

```bash
python validate_pipeline.py
```

**Expected Output:**

```text
✅ PASSED: All checks passed successfully!
```

---

### 🧪 Automated Tests

Run integration tests using pytest.

```bash
python -m pytest tests/
```

**Expected Output:**

```text
===== 2 passed in 1.05s =====
```

---

## ⚡ API Usage

### 🔁 Using CURL

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

* The model is trained **inside the Docker image during build**
* Do **NOT** mount a Windows-generated `mlflow.db` into Docker
* Always rebuild using:

```bash
docker build --no-cache -t sales-classifier:v1 .
```
