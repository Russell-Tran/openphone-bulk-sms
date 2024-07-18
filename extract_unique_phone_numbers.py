import pandas as pd
import json
import re
from tqdm import tqdm

# Load configuration from config_extract_phones.json
with open('config_extract_phones.json') as config_file:
    config = json.load(config_file)

# Read CSV files with progress bar
print("Reading CSV files...")
contacts_df = pd.read_csv(config['contacts_csv'])
calls_df = pd.read_csv(config['calls_csv'])
messages_df = pd.read_csv(config['messages_csv'])

# Extract phone numbers from contacts with data cleaning
print("Extracting phone numbers from contacts...")
contacts_phone_numbers = []
for numbers in tqdm(contacts_df[['phone_number_1', 'phone_number_2']].values.flatten()):
    if pd.notna(numbers):
        contacts_phone_numbers.extend(str(numbers).split(','))

# Extract phone numbers from calls with data cleaning
print("Extracting phone numbers from calls...")
calls_phone_numbers = []
for numbers in tqdm(calls_df[['to', 'from']].values.flatten()):
    if pd.notna(numbers):
        calls_phone_numbers.extend(str(numbers).split(','))

# Extract phone numbers from messages with data cleaning
print("Extracting phone numbers from messages...")
messages_phone_numbers = []
for numbers in tqdm(messages_df[['to', 'from']].values.flatten()):
    if pd.notna(numbers):
        messages_phone_numbers.extend(str(numbers).split(','))

# Combine all phone numbers and remove duplicates
print("Combining and removing duplicates...")
all_phone_numbers = pd.Series(contacts_phone_numbers + calls_phone_numbers + messages_phone_numbers).dropna().unique()

# Create a DataFrame for unique phone numbers
unique_phone_numbers_df = pd.DataFrame(all_phone_numbers, columns=['phone_number'])

# Save the unique phone numbers to a CSV file
unique_phone_numbers_df.to_csv(config['output_csv'], index=False)

# Verify uniqueness by reading the CSV file back and checking for duplicates
print("Verifying uniqueness of phone numbers in the output CSV...")
output_df = pd.read_csv(config['output_csv'])
duplicate_phone_numbers = output_df[output_df.duplicated(subset='phone_number', keep=False)]

if duplicate_phone_numbers.empty:
    print("Verification complete: All phone numbers are unique.")
else:
    print("Verification failed: There are duplicate phone numbers in the output CSV.")
    print(duplicate_phone_numbers)

# Verify phone number format
print("Verifying phone number formats...")
phone_number_pattern = re.compile(r'^\+?\d{10,15}$')
invalid_phone_numbers = output_df[~output_df['phone_number'].apply(lambda x: bool(phone_number_pattern.match(x)))]

if invalid_phone_numbers.empty:
    print("Verification complete: All entries are valid phone numbers.")
else:
    print("Verification failed: There are invalid phone numbers in the output CSV.")
    print(invalid_phone_numbers)

print(f"Unique phone numbers have been extracted and saved to {config['output_csv']}")
