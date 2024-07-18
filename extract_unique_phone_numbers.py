import pandas as pd
import json
import re
from tqdm import tqdm

# Load configuration from config_extract_phones.json
with open('config_extract_phones.json') as config_file:
    config = json.load(config_file)

# Read CSV files with progress bar
contacts_df = pd.read_csv(config['contacts_csv'])
calls_df = pd.read_csv(config['calls_csv'])
messages_df = pd.read_csv(config['messages_csv'])

# Extract phone numbers from contacts with data cleaning
contacts_phone_numbers = []
for numbers in tqdm(contacts_df[['phone_number_1', 'phone_number_2']].values.flatten()):
    if pd.notna(numbers):
        contacts_phone_numbers.extend(str(numbers).split(','))

# Extract phone numbers from calls with data cleaning
calls_phone_numbers = []
for numbers in tqdm(calls_df[['to', 'from']].values.flatten()):
    if pd.notna(numbers):
        calls_phone_numbers.extend(str(numbers).split(','))

# Extract phone numbers from messages with data cleaning
messages_phone_numbers = []
for numbers in tqdm(messages_df[['to', 'from']].values.flatten()):
    if pd.notna(numbers):
        messages_phone_numbers.extend(str(numbers).split(','))

# Combine all phone numbers and remove duplicates
all_phone_numbers = pd.Series(contacts_phone_numbers + calls_phone_numbers + messages_phone_numbers).dropna().drop_duplicates()

# Verify the phone number format and identify invalid ones
phone_number_pattern = re.compile(r'^\+?\d{10,15}$')
valid_phone_numbers = []
invalid_phone_numbers = []

for num in all_phone_numbers:
    if phone_number_pattern.match(str(num)):
        valid_phone_numbers.append(num)
    else:
        invalid_phone_numbers.append(num)

# Print invalid phone numbers
if invalid_phone_numbers:
    print("Invalid phone numbers:")
    for invalid_number in invalid_phone_numbers:
        print(invalid_number)

# Create a DataFrame for valid unique phone numbers
unique_phone_numbers_df = pd.DataFrame(valid_phone_numbers, columns=['phone_number']).drop_duplicates()

# Save the unique phone numbers to a CSV file
unique_phone_numbers_df.to_csv(config['output_csv'], index=False)

# Verify uniqueness by reading the CSV file back, checking for duplicates, and re-saving if necessary
output_df = pd.read_csv(config['output_csv'])
output_df = output_df.drop_duplicates(subset='phone_number')
output_df.to_csv(config['output_csv'], index=False)

# Verify uniqueness by reading the CSV file again and checking for duplicates
final_output_df = pd.read_csv(config['output_csv'])
if final_output_df.duplicated(subset='phone_number').sum() == 0:
    print("Verification complete: All phone numbers are unique.")
else:
    print("Verification failed: There are duplicate phone numbers in the output CSV.")

# Verify phone number format
final_output_df['phone_number'] = final_output_df['phone_number'].astype(str)  # Ensure all are strings
invalid_phone_numbers_final = final_output_df[~final_output_df['phone_number'].apply(lambda x: bool(phone_number_pattern.match(x)))]

if invalid_phone_numbers_final.empty:
    print("Verification complete: All entries are valid phone numbers.")
else:
    print("Verification failed: There are invalid phone numbers in the output CSV.")
    print(invalid_phone_numbers_final)

print(f"Unique phone numbers have been extracted and saved to {config['output_csv']}")
