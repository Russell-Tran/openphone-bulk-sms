import requests
import json
import pandas as pd

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Get the URL for the Zapier webhook and CSV path from the configuration
webhook_url = config['webhook_url']
csv_path = config['csv_path']

# Read the CSV file
df = pd.read_csv(csv_path)

# Extract phone numbers into a comma-delimited string without spaces
phone_numbers = ','.join(df['phone_number'].astype(str).tolist())

# Define the data payload
data = {
    "phone_numbers": phone_numbers,
    "batch_name": "HARDCODE A"
}

# Send the POST request to the webhook
response = requests.post(webhook_url, json=data)

# Print the response status code and text
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
