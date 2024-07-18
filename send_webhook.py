import requests
import json
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import pytz
import logging
import time

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# Get the URL for the Zapier webhook, CSV path, and sleep interval from the configuration
webhook_url = config['webhook_url']
csv_path = config['csv_path']
sleep_interval = config.get('sleep_interval', 3)  # Default to 3 seconds if not specified

# Read the CSV file
df = pd.read_csv(csv_path)

# Initialize logging
logging.basicConfig(filename='request_log.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Ensure 'timestamp', 'status_code', 'response_text', and 'error_message' columns exist
if 'timestamp' not in df.columns:
    df['timestamp'] = pd.NaT
if 'status_code' not in df.columns:
    df['status_code'] = pd.NA
if 'response_text' not in df.columns:
    df['response_text'] = pd.NA
if 'error_message' not in df.columns:
    df['error_message'] = pd.NA

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Get the current time in Los Angeles time zone
la_timezone = pytz.timezone('America/Los_Angeles')

# Iterate over each phone number and send the request
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    phone_number = row['phone_number']

    # Check if the request has already been made by checking if timestamp exists
    if not pd.isnull(row['timestamp']):
        continue

    # Convert the phone number to a string
    phone_number_str = str(phone_number)

    # Define the data payload
    data = {
        "phone_number": phone_number_str,
    }

    try:
        # Send the POST request to the webhook
        response = requests.post(webhook_url, json=data)

        # Log the response using tqdm.write
        log_message = f"Phone number: {phone_number_str}, Status Code: {response.status_code}, Response Text: {response.text}"
        logging.info(log_message)
        tqdm.write(log_message)

        # Get current time in Los Angeles time zone
        current_time = datetime.now(la_timezone)

        # Save the response status, text, and timestamp to the DataFrame
        df.at[index, 'status_code'] = response.status_code
        df.at[index, 'response_text'] = response.text
        df.at[index, 'timestamp'] = current_time

    except Exception as e:
        error_message = f"Error for phone number: {phone_number_str}, Error: {str(e)}"
        logging.error(error_message)
        tqdm.write(error_message)

        # Save the error message to the DataFrame
        df.at[index, 'error_message'] = str(e)

    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_path, index=False)

    # Sleep for the configured interval before the next request
    time.sleep(sleep_interval)

print("Completed processing all phone numbers.")
