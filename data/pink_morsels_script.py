import pandas as pd

# List your 3 CSV file names
input_files = ["daily_sales_data_0.csv", "daily_sales_data_1.csv","daily_sales_data_2.csv"]  

# Create an empty list to store filtered DataFrames
all_data = []

# Process each file
for file in input_files:
    df = pd.read_csv(file)

    # Filter for 'pink morsel'
    df = df[df['product'].str.lower() == 'pink morsel']

    # Clean price and calculate sales
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df['sales'] = df['price'] * df['quantity']

    # Keep only sales, date, region
    filtered = df[['sales', 'date', 'region']]

    # Add to the combined list
    all_data.append(filtered)

# Combine all filtered data into one DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Save to a single CSV file
final_df.to_csv("pink_morsel_sales_combined.csv", index=False)

print("✅ pink_morsel_sales_combined.csv created successfully.")
