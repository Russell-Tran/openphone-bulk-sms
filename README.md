# OpenPhone Bulk SMS

When you need to send a bulk SMS to your customers on OpenPhone in a one-off instance, such as notifying them of changing your phone number or shutting it down. Please use responsibly. 

<img src="zapier.png" alt="Zapier" width="400">

## Overview

This project consists of two main parts:

1. **Extracting Unique Phone Numbers**: This part involves extracting unique phone numbers from your OpenPhone data exports.
2. **Bulk SMS Webhook Sender**: This part involves sending SMS messages to the extracted phone numbers via a Zapier webhook.

## Part 1: Extracting Unique Phone Numbers

To extract all unique phone numbers from your OpenPhone data, follow these steps:

### Step 1: Export Your Data

Export your contacts, calls, and messages data from OpenPhone and receive them as CSV files.

### Step 2: Configuration

Create a configuration file named `config_extract_phones.json` with the following content:
```json
{
    "contacts_csv": "path/to/your/contacts.csv",
    "calls_csv": "path/to/your/calls.csv",
    "messages_csv": "path/to/your/messages.csv",
    "output_csv": "unique_phone_numbers.csv"
}
```

### Step 3: Run the Script

To extract unique phone numbers from the exported OpenPhone data, run the script with the following command:

```bash
python extract_unique_phone_numbers.py
```

Ensure you have the `config_extract_phones.json` file properly configured as mentioned above.

## Part 2: Bulk SMS Webhook Sender

The main goal of this project is to send bulk SMS messages. Since OpenPhone does not have an API but does have Zapier integration, we use a Zapier webhook to trigger sending messages in OpenPhone.

<img src="zapier.png" alt="Zapier" width="400">


### Configuration

Create a configuration file (`config.json`) with the following content:

**config.json**:
```json
{
    "webhook_url": "YOUR_ZAPIER_WEBHOOK_URL",
    "csv_path": "path/to/your/csvfile.csv",
    "sleep_interval": 3
}
```

The CSV should have one column called `phone_number`.

### Features

- **Reads phone numbers from a CSV file**: The CSV file must have a column named `phone_number`.
- **Sends POST requests to a webhook**: The script sends each phone number to a specified Zapier webhook URL that triggers an SMS in OpenPhone.
- **Fault tolerance**:
  - Logs responses and errors to a log file.
  - Saves response status, response text, and timestamp to the CSV file after each request.
  - Skips phone numbers that have already been processed, based on the presence of a timestamp.
- **Progress bar**: Uses tqdm to display a progress bar for the processing of phone numbers.
- **Configurable sleep interval**: The sleep interval between requests can be set in the configuration file.
- **Handles missing columns**: Ensures that required columns (`timestamp`, `status_code`, `response_text`, and `error_message`) exist in the CSV file.

### CSV File

The CSV file should have at least one column named `phone_number`. The script will add the following columns if they do not exist:

- `timestamp`: The timestamp when the phone number was processed.
- `status_code`: The HTTP status code returned by the webhook.
- `response_text`: The response text returned by the webhook.
- `error_message`: Any error message encountered during the request.

### Usage

To run the script, use the following command:

```bash
python send_webhook.py
```

Ensure you have the `config.json` file properly configured as mentioned above. This script will read the phone numbers from the CSV file and send each number to the specified Zapier webhook, which in turn sends an SMS through OpenPhone.
