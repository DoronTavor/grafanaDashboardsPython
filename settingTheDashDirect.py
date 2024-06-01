import requests
import json

# Set your Grafana credentials and URL
GRAFANA_URL = "http://your-grafana-instance/api/dashboards/db"
GRAFANA_API_KEY = "your-grafana-api-key"

# Define the headers and payload
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GRAFANA_API_KEY}"
}

payload = {
    "dashboard": dashboard_json,
    "folderId": 0,  # Use the appropriate folder ID
    "overwrite": True  # Overwrite the existing dashboard if it exists
}

# Make the API request to create/update the dashboard
response = requests.post(GRAFANA_URL, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("Dashboard uploaded successfully.")
else:
    print(f"Failed to upload dashboard. Status code: {response.status_code}")
    print(response.json())
