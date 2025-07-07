import pandas as pd
import os

# Path to the data folder (one level up from scripts)
data_folder = os.path.join("..", "data")

# List your CSV file names
input_files = [
    "daily_sales_data_0.csv",
    "daily_sales_data_1.csv",
    "daily_sales_data_2.csv"
]

# Create an empty list to store filtered DataFrames
all_data = []

# Process each file
for file in input_files:
    file_path = os.path.join(data_folder, file)  # full path to input file
    df = pd.read_csv(file_path)

    # Filter for 'pink morsel'
    df = df[df['product'].str.lower() == 'pink morsel']

    # Clean price and calculate sales
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df['sales'] = df['price'] * df['quantity']

    # Keep only sales, date, region
    filtered = df[['sales', 'date', 'region']]
    all_data.append(filtered)

# Combine all filtered data into one DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Output path in the data folder
output_path = os.path.join(data_folder, "pink_morsel_sales_combined.csv")
final_df.to_csv(output_path, index=False)

print("✅ pink_morsel_sales_combined.csv created successfully in the data folder.")
