import pandas as pd

# Specify the input file path
input_file = 'filtered_data.csv'  # Replace with your actual input file path

# Read the CSV file
df = pd.read_csv(input_file)

# Update the date column name based on the actual column in your file
date_column = 't_dat'  # Replace with the correct column name if different

# Ensure the date column exists and is in datetime format
if date_column in df.columns:
    df[date_column] = pd.to_datetime(df[date_column])

    # Define the start and end date for filtering
    start_date = pd.Timestamp('2018-10-11')
    end_date = start_date + pd.Timedelta(days=365)

    # Filter the DataFrame for "Sweater" in the specified date range
    sweater_df = df[
        (df['product_type_name'] == 'Sweater') &
        (df[date_column] >= start_date) & 
        (df[date_column] <= end_date)
    ]

    # Group by 'prod_name' and count occurrences to find the top 10 by frequency
    top_10_prod_names = sweater_df['prod_name'].value_counts().head(10)

    # Display the top 10 'prod_name' by frequency
    print("Top 10 prod_name by frequency for product_type_name 'Sweater' within 10 days after 10/10/2022:")
    print(top_10_prod_names)
else:
    print(f"'{date_column}' column not found in the file. Please check the CSV file.")
