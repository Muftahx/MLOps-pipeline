import requests
import time
import sys

# Configuration
URL = "http://localhost:8000/predict"
MAX_RETRIES = 10
WAIT_SECONDS = 5

# Sample JSON payload (Matched to your test_api.py structure)
payload = {
    "Date": "2023-01-01",
    "BranchID": "B001",
    "InvoiceNumber": "INV-1001",
    "ItemCode": "ITEM-500",
    "QuantitySold": 1.0
}

print(f"🚀 Starting Smoke Test on {URL}...")
print(f"Payload: {payload}")

for i in range(MAX_RETRIES):
    try:
        response = requests.post(URL, json=payload)
        
        if response.status_code == 200:
            print("✅ SMOKE TEST PASSED: Service returned 200 OK.")
            print(f"Response: {response.json()}")
            sys.exit(0) # Success exit code
        else:
            print(f"⚠️ Service up but returned {response.status_code}. Retrying...")
            print(f"Details: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"⏳ Attempt {i+1}/{MAX_RETRIES}: Service not ready yet...")
    
    time.sleep(WAIT_SECONDS)

print("❌ SMOKE TEST FAILED: Service did not respond in time.")
sys.exit(1) # Failure exit code