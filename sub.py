import pandas as pd
from datetime import datetime, timedelta

# Function to calculate the start date based on the final date and number of days
def get_start_date_from_final_date(final_date, days):
    final_date_obj = datetime.strptime(final_date, '%Y-%m-%d')
    start_date_obj = final_date_obj - timedelta(days=days)
    return start_date_obj.strftime('%Y-%m-%d')

# Function to calculate daily frequency of product categories including sales and turnover
def calculate_daily_sales_and_turnover_single_category(csv_file, final_date, days, category):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Get the start date from the final date and number of days
    start_date = get_start_date_from_final_date(final_date, days)
    end_date = final_date  # Final date is considered the end date

    # Filter the dataset by the given date range
    df['t_dat'] = pd.to_datetime(df['t_dat'], format='%Y-%m-%d')
    mask = (df['t_dat'] >= start_date) & (df['t_dat'] <= end_date)
    filtered_df = df[mask]

    # Initialize a dictionary to store the daily sales, turnover, highest product, and product_type_name
    daily_sales_turnover = {
        "date": [],
        f"{category}_sales": [],
        f"{category}_turnover": [],
        "highest_product": [],
        "product_type_name": [],
    }

    # Loop through each day in the range and calculate sales and turnover for the category
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    while current_date <= end_date_obj:
        # Filter rows for the current date
        day_str = current_date.strftime('%Y-%m-%d')
        daily_df = filtered_df[filtered_df['t_dat'] == current_date]

        # Calculate the sales for the category
        category_sales = daily_df[daily_df['product_group_name'] == category]['sales_1_days'].sum()

        # Calculate the turnover for the category by multiplying sales with price_per_sale
        category_turnover = (daily_df[daily_df['product_group_name'] == category]
                             ['sales_1_days'] * daily_df['price_per_sale']).sum()

        # Find the highest selling product for the category on the current day
        highest_product_df = daily_df[daily_df['product_group_name'] == category]
        if not highest_product_df.empty:
            highest_product_sales = highest_product_df.groupby('product_group_name')['sales_1_days'].sum()
            highest_product_name = highest_product_sales.idxmax()

            # Get the product_type_name of the highest selling product
            highest_product_type = highest_product_df[highest_product_df['product_group_name'] == highest_product_name].iloc[0]['product_type_name']
        else:
            highest_product_name = ""
            highest_product_type = ""

        # Append the sales, turnover, and highest product info to the dictionary
        daily_sales_turnover["date"].append(day_str)
        daily_sales_turnover[f"{category}_sales"].append(category_sales)
        daily_sales_turnover[f"{category}_turnover"].append(category_turnover)
        daily_sales_turnover["highest_product"].append(highest_product_name)
        daily_sales_turnover["product_type_name"].append(highest_product_type)

        # Move to the next day
        current_date += timedelta(days=1)

    # Convert the dictionary to a DataFrame
    result_df = pd.DataFrame(daily_sales_turnover)

    # Calculate the total turnover for the category
    total_turnover = result_df[f"{category}_turnover"].sum()

    # Append the total turnover as a final row in the DataFrame
    result_df.loc[len(result_df)] = {
        "date": "Total",
        f"{category}_sales": result_df[f"{category}_sales"].sum(),
        f"{category}_turnover": total_turnover,
        "highest_product": "",
        "product_type_name": "",
    }

    # Return the daily sales, turnover, highest product, and product type name as a DataFrame
    return result_df

# Example usage
csv_file = 'filtered_data_top_10.csv'  # Update this with the path to your CSV file
final_date = '2020-01-05'  # Final date (e.g., '2025-01-05')
days = 5  # Number of days to go back
category = "Shoes"  # The category to analyze

# Calculate and print the daily sales, turnover, highest product, and product type
result_df = calculate_daily_sales_and_turnover_single_category(csv_file, final_date, days, category)

print(result_df)
