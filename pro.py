import pandas as pd

# Load the data into a DataFrame (replace with your actual file path)
df = pd.read_csv('filtered_data_top_10.csv')

# Define the product categories you are interested in
category_products = ['Garment Upper body', 'T-shirt']

# Filter the DataFrame to include only rows that match the specified product categories
filtered_df = df[df['product_group_name'].isin(category_products)].copy()

# Check if the columns needed for calculations (sales_1_days, price_per_sale) contain valid data
filtered_df = filtered_df.dropna(subset=['sales_1_days', 'price_per_sale'])  # Remove rows with NaN sales or price values

# Check if we have any rows remaining after filtering
if filtered_df.empty:
    print("No data found for the specified product categories.")
else:
    # Group by date and calculate daily sales and turnover
    daily_sales_turnover = filtered_df.groupby('date').apply(
        lambda x: pd.Series({
            'Garment Upper body_sales': x['sales_1_days'].sum(),
            'Garment Upper body_turnover': (x['sales_1_days'] * x['price_per_sale']).sum()
        })
    ).reset_index()

    # Check for any zeros in sales and turnover
    print("Daily Sales and Turnover Calculation for each date:")
    for index, row in daily_sales_turnover.iterrows():
        print(f"Date: {row['date']}, Sales: {row['Garment Upper body_sales']}, Turnover: {row['Garment Upper body_turnover']}")

    # Calculate total sales and turnover
    total_sales = daily_sales_turnover['Garment Upper body_sales'].sum()
    total_turnover = daily_sales_turnover['Garment Upper body_turnover'].sum()

    print("\nTotal Sales and Turnover for the product category:")
    print(f"Total Sales: {total_sales}")
    print(f"Total Turnover: {total_turnover}")

    # Create a final DataFrame with the total sales and turnover
    total_row = pd.DataFrame({
        'date': ['Total'],
        'Garment Upper body_sales': [total_sales],
        'Garment Upper body_turnover': [total_turnover]
    })

    # Append the total row to the daily sales and turnover
    final_df = pd.concat([daily_sales_turnover, total_row], ignore_index=True)

    # Print final DataFrame with sales and turnover for each day and the total row
    print("\nFinal DataFrame:")
    print(final_df)

    # Optional: Save the final DataFrame to a CSV file
    final_df.to_csv('sales_turnover_summary.csv', index=False)
