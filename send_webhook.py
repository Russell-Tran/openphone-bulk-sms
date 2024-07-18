import requests
import json

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Get the URL for the Zapier webhook and phone number from the configuration
webhook_url = config['webhook_url']
phone_number = config['phone_number']

# Define the data payload
data = {
    "phone_number": phone_number
}

# Send the POST request to the webhook
response = requests.post(webhook_url, json=data)

# Print the response status code and text
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
