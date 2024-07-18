import pandas as pd
import json

# Load configuration from config_extract_phones.json
with open('config_extract_phones.json') as config_file:
    config = json.load(config_file)

# Read CSV files
contacts_df = pd.read_csv(config['contacts_csv'])
calls_df = pd.read_csv(config['calls_csv'])
messages_df = pd.read_csv(config['messages_csv'])

# Extract phone numbers from contacts
contacts_phone_numbers = contacts_df[['phone_number_1', 'phone_number_2']].values.flatten()

# Extract phone numbers from calls
calls_phone_numbers = calls_df[['to', 'from']].values.flatten()

# Extract phone numbers from messages
messages_phone_numbers = messages_df[['to', 'from']].values.flatten()

# Combine all phone numbers and remove duplicates
all_phone_numbers = pd.Series(contacts_phone_numbers.tolist() + calls_phone_numbers.tolist() + messages_phone_numbers.tolist()).dropna().unique()

# Create a DataFrame for unique phone numbers
unique_phone_numbers_df = pd.DataFrame(all_phone_numbers, columns=['phone_number'])

# Save the unique phone numbers to a CSV file
unique_phone_numbers_df.to_csv(config['output_csv'], index=False)

print(f"Unique phone numbers have been extracted and saved to {config['output_csv']}")
