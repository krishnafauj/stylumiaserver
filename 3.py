import pandas as pd

# Specify the input file path
input_file = 'updated_file.csv'  # Replace with your actual input file path

# Read the CSV file
df = pd.read_csv(input_file)

# Ensure 'price_scaled_sum' and 'sales_1_days' columns exist in the DataFrame
if 'price_scaled_sum' in df.columns and 'sales_1_days' in df.columns:
    # Calculate the new 'price_per_sale' column and convert it to integer
    df['price_per_sale'] = (df['price_scaled_sum'] / df['sales_1_days']).fillna(0).astype(int)

    # Drop the 'price_scaled_sum' and 'sales_1_days' columns
    df.drop(['price_scaled_sum', 'sales_1_days'], axis=1, inplace=True)

    # Save the updated DataFrame back to the same CSV file, overwriting it
    df.to_csv(input_file, index=False)

    print(f"The 'price_scaled_sum' and 'sales_1_days' columns have been dropped, and the 'price_per_sale' column is added in the file: {input_file}")
else:
    print("'price_scaled_sum' or 'sales_1_days' column not found in the file.")
