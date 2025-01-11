import pandas as pd
from datetime import datetime, timedelta

# Function to calculate the start date based on the final date and number of days
def get_start_date_from_final_date(final_date, days):
    final_date_obj = datetime.strptime(final_date, '%Y-%m-%d')
    start_date_obj = final_date_obj - timedelta(days=days)
    return start_date_obj.strftime('%Y-%m-%d')

# Function to calculate daily frequency of product categories including sales and turnover for two categories
def calculate_daily_sales_and_turnover_comparison(csv_file, final_date, days, category1, category2):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Get the start date from the final date and number of days
    start_date = get_start_date_from_final_date(final_date, days)
    end_date = final_date  # Final date is considered the end date

    # Filter the dataset by the given date range
    df['t_dat'] = pd.to_datetime(df['t_dat'], format='%Y-%m-%d')
    mask = (df['t_dat'] >= start_date) & (df['t_dat'] <= end_date)
    filtered_df = df[mask]

    # Initialize a dictionary to store the daily sales, turnover, highest product, and product_type_name for both categories
    daily_sales_turnover = {
        "date": [],
        f"{category1}_sales": [],
        f"{category1}_turnover": [],
        f"{category2}_sales": [],
        f"{category2}_turnover": [],
        "highest_product_1": [],
        "product_type_name_1": [],
        "highest_product_2": [],
        "product_type_name_2": [],
    }

    # Loop through each day in the range and calculate sales and turnover for both categories
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    while current_date <= end_date_obj:
        # Filter rows for the current date
        day_str = current_date.strftime('%Y-%m-%d')
        daily_df = filtered_df[filtered_df['t_dat'] == current_date]

        # Calculate the sales and turnover for both categories
        category1_sales = daily_df[daily_df['product_group_name'] == category1]['sales_1_days'].sum()
        category2_sales = daily_df[daily_df['product_group_name'] == category2]['sales_1_days'].sum()

        category1_turnover = (daily_df[daily_df['product_group_name'] == category1]
                              ['sales_1_days'] * daily_df['price_per_sale']).sum()
        category2_turnover = (daily_df[daily_df['product_group_name'] == category2]
                              ['sales_1_days'] * daily_df['price_per_sale']).sum()

        # Find the highest selling products for both categories on the current day
        highest_product_df_1 = daily_df[daily_df['product_group_name'] == category1]
        highest_product_df_2 = daily_df[daily_df['product_group_name'] == category2]

        # Get highest product for category 1
        if not highest_product_df_1.empty:
            highest_product_sales_1 = highest_product_df_1.groupby('product_group_name')['sales_1_days'].sum()
            highest_product_name_1 = highest_product_sales_1.idxmax()
            highest_product_type_1 = highest_product_df_1[highest_product_df_1['product_group_name'] == highest_product_name_1].iloc[0]['product_type_name']
        else:
            highest_product_name_1 = ""
            highest_product_type_1 = ""

        # Get highest product for category 2
        if not highest_product_df_2.empty:
            highest_product_sales_2 = highest_product_df_2.groupby('product_group_name')['sales_1_days'].sum()
            highest_product_name_2 = highest_product_sales_2.idxmax()
            highest_product_type_2 = highest_product_df_2[highest_product_df_2['product_group_name'] == highest_product_name_2].iloc[0]['product_type_name']
        else:
            highest_product_name_2 = ""
            highest_product_type_2 = ""

        # Append the sales, turnover, and highest product info to the dictionary
        daily_sales_turnover["date"].append(day_str)
        daily_sales_turnover[f"{category1}_sales"].append(category1_sales)
        daily_sales_turnover[f"{category1}_turnover"].append(category1_turnover)
        daily_sales_turnover[f"{category2}_sales"].append(category2_sales)
        daily_sales_turnover[f"{category2}_turnover"].append(category2_turnover)
        daily_sales_turnover["highest_product_1"].append(highest_product_name_1)
        daily_sales_turnover["product_type_name_1"].append(highest_product_type_1)
        daily_sales_turnover["highest_product_2"].append(highest_product_name_2)
        daily_sales_turnover["product_type_name_2"].append(highest_product_type_2)

        # Move to the next day
        current_date += timedelta(days=1)

    # Convert the dictionary to a DataFrame
    result_df = pd.DataFrame(daily_sales_turnover)

    # Calculate the total turnover for both categories
    total_turnover_1 = result_df[f"{category1}_turnover"].sum()
    total_turnover_2 = result_df[f"{category2}_turnover"].sum()

    # Append the total turnover as a final row in the DataFrame
    result_df.loc[len(result_df)] = {
        "date": "Total",
        f"{category1}_sales": result_df[f"{category1}_sales"].sum(),
        f"{category1}_turnover": total_turnover_1,
        f"{category2}_sales": result_df[f"{category2}_sales"].sum(),
        f"{category2}_turnover": total_turnover_2,
        "highest_product_1": "",
        "product_type_name_1": "",
        "highest_product_2": "",
        "product_type_name_2": "",
    }

    # Return the daily sales, turnover, highest product, and product type name for both categories as a DataFrame
    return result_df

# Example usage
csv_file = 'filtered_data_top_10.csv'  # Update this with the path to your CSV file
final_date = '2020-01-05'  # Final date (e.g., '2025-01-05')
days = 5  # Number of days to go back
category1 = "Shoes"  # The first category to analyze
category2 = "Bags"  # The second category to analyze

# Calculate and print the daily sales, turnover, highest product, and product type for both categories
result_df = calculate_daily_sales_and_turnover_comparison(csv_file, final_date, days, category1, category2)

print(result_df)
