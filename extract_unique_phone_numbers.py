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
print("Combining phone numbers and removing duplicates...")
all_phone_numbers = pd.Series(contacts_phone_numbers + calls_phone_numbers + messages_phone_numbers).dropna()

# Test for duplicates before removing them
print(f"Total phone numbers before removing duplicates: {len(all_phone_numbers)}")
print(f"Number of duplicates before removing: {all_phone_numbers.duplicated().sum()}")

# Remove duplicates
all_phone_numbers = all_phone_numbers.drop_duplicates()

# Test for duplicates after removing them
print(f"Total phone numbers after removing duplicates: {len(all_phone_numbers)}")
print(f"Number of duplicates after removing: {all_phone_numbers.duplicated().sum()}")

# Verify the phone number format and if there are invalid ones, remove them, then also tell us which ones you removed
print("Verifying phone number formats and removing invalid ones...")
phone_number_pattern = re.compile(r'^\+?\d{10,15}$')
valid_phone_numbers = []
invalid_phone_numbers = []

for phone_number in all_phone_numbers:
    if phone_number_pattern.match(str(phone_number)):
        valid_phone_numbers.append(phone_number)
    else:
        invalid_phone_numbers.append(phone_number)

print(f"Total valid phone numbers: {len(valid_phone_numbers)}")
print(f"Total invalid phone numbers: {len(invalid_phone_numbers)}")

if invalid_phone_numbers:
    print("Removing invalid phone numbers:")
    for invalid_number in invalid_phone_numbers:
        print(invalid_number)

# Test for duplicates in valid_phone_numbers
valid_phone_numbers_series = pd.Series(valid_phone_numbers)
print(f"Number of duplicates in valid phone numbers: {valid_phone_numbers_series.duplicated().sum()}")

# Create a DataFrame for valid unique phone numbers
# unique_phone_numbers_df = pd.DataFrame(valid_phone_numbers, columns=['phone_number']).drop_duplicates()
unique_phone_numbers_df = pd.DataFrame(valid_phone_numbers, columns=['phone_number'])

# Test for duplicates in unique_phone_numbers_df
print(f"Total unique phone numbers: {len(unique_phone_numbers_df)}")
print(f"Number of duplicates in unique phone numbers: {unique_phone_numbers_df.duplicated().sum()}")

# Save the unique phone numbers to a CSV file
unique_phone_numbers_df.to_csv(config['output_csv'], index=False)

# Verify uniqueness by reading the CSV file back and checking for duplicates
print("Verifying uniqueness of phone numbers in the output CSV...")
output_df = pd.read_csv(config['output_csv'])
output_df = output_df.drop_duplicates()  # Drop duplicates again just in case

duplicate_phone_numbers = output_df[output_df.duplicated(subset='phone_number', keep=False)]

if duplicate_phone_numbers.empty:
    print("Verification complete: All phone numbers are unique.")
else:
    print("Verification failed: There are duplicate phone numbers in the output CSV.")
    print(duplicate_phone_numbers)

# Verify phone number format
print("Verifying phone number formats...")
output_df['phone_number'] = output_df['phone_number'].astype(str)  # Ensure all are strings
invalid_phone_numbers = output_df[~output_df['phone_number'].apply(lambda x: bool(phone_number_pattern.match(x)))]

if invalid_phone_numbers.empty:
    print("Verification complete: All entries are valid phone numbers.")
else:
    print("Verification failed: There are invalid phone numbers in the output CSV.")
    print(invalid_phone_numbers)

print(f"Unique phone numbers have been extracted and saved to {config['output_csv']}")
