import pandas as pd
from datetime import datetime, timedelta

# Function to calculate the start date based on final date and number of days
def get_start_date_from_final_date(final_date, days):
    final_date_obj = datetime.strptime(final_date, '%Y-%m-%d')
    start_date_obj = final_date_obj - timedelta(days=days)
    return start_date_obj.strftime('%Y-%m-%d')
# Function to calculate daily sales and turnover for selected categories
# Function to calculate daily sales and turnover for selected categories
def calculate_daily_sales_and_turnover(final_date, days, category1, category2):
    # Read the CSV file into a DataFrame
    csv_file = 'filtered_data_top_10.csv'
    df = pd.read_csv(csv_file)
    
    # Define the categories
    categories = {
        "Clothing": ["Garment Upper body", "Garment Lower body", "Garment Full body"],
        "Footwear & Accessories": ["Shoes", "Socks & Tights", "Accessories", "Bags", "Garment and Shoe care"],
        "Home & Other Goods": ["Furniture", "Stationery", "Interior textile", "Items", "Cosmetic", "Unknown", "Fun"],
        "Undergarments": ["Underwear", "Underwear/nightwear", "Swimwear", "Nightwear"]
    }

    # Check if provided categories are valid
    if category1 not in categories or category2 not in categories:
        raise ValueError("Invalid category names provided")

    # Get the start date from the final date and number of days
    start_date = get_start_date_from_final_date(final_date, days)
    end_date = final_date  # Final date is considered the end date

    # Filter the dataset by the given date range
    df['t_dat'] = pd.to_datetime(df['t_dat'], format='%Y-%m-%d')
    mask = (df['t_dat'] >= start_date) & (df['t_dat'] <= end_date)
    filtered_df = df[mask]

    if filtered_df.empty:
        return "No data found for the specified date range"

    # Get the list of products for the two selected categories
    category1_products = categories[category1]
    category2_products = categories[category2]

    # Initialize a dictionary to store the daily sales, turnover, highest product, and product_type_name
    daily_sales_turnover = {
        "date": [],
        f"{category1}_sales": [],
        f"{category2}_sales": [],
        f"{category1}_turnover": [],
        f"{category2}_turnover": [],
        "highest_product_category1": [],
        "highest_product_category2": [],
        "product_type_name_category1": [],
        "product_type_name_category2": [],
    }

    # Loop through each day in the range and calculate sales and turnover for each category
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    while current_date <= end_date_obj:
        # Filter rows for the current date
        day_str = current_date.strftime('%Y-%m-%d')
        daily_df = filtered_df[filtered_df['t_dat'] == current_date]

        # Calculate the sales and turnover for each category
        category1_sales = daily_df[daily_df['product_group_name'].isin(category1_products)]['sales_1_days'].sum()
        category2_sales = daily_df[daily_df['product_group_name'].isin(category2_products)]['sales_1_days'].sum()

        category1_turnover = (daily_df[daily_df['product_group_name'].isin(category1_products)]
                              ['sales_1_days'] * daily_df['price_per_sale']).sum()
        category2_turnover = (daily_df[daily_df['product_group_name'].isin(category2_products)]
                              ['sales_1_days'] * daily_df['price_per_sale']).sum()

        # Find the highest selling product for each category on the current day
        highest_product_category1 = daily_df[daily_df['product_group_name'].isin(category1_products)]
        if not highest_product_category1.empty:
            highest_product_category1_sales = highest_product_category1.groupby('product_group_name')['sales_1_days'].sum()
            highest_product_category1_name = highest_product_category1_sales.idxmax()
            highest_product_category1_type = highest_product_category1[highest_product_category1['product_group_name'] == highest_product_category1_name].iloc[0]['product_type_name']
        else:
            highest_product_category1_name = ""
            highest_product_category1_type = ""

        highest_product_category2 = daily_df[daily_df['product_group_name'].isin(category2_products)]
        if not highest_product_category2.empty:
            highest_product_category2_sales = highest_product_category2.groupby('product_group_name')['sales_1_days'].sum()
            highest_product_category2_name = highest_product_category2_sales.idxmax()
            highest_product_category2_type = highest_product_category2[highest_product_category2['product_group_name'] == highest_product_category2_name].iloc[0]['product_type_name']
        else:
            highest_product_category2_name = ""
            highest_product_category2_type = ""

        # Append the sales, turnover, and highest product info to the dictionary
        daily_sales_turnover["date"].append(day_str)
        daily_sales_turnover[f"{category1}_sales"].append(category1_sales)
        daily_sales_turnover[f"{category2}_sales"].append(category2_sales)
        daily_sales_turnover[f"{category1}_turnover"].append(category1_turnover)
        daily_sales_turnover[f"{category2}_turnover"].append(category2_turnover)
        daily_sales_turnover["highest_product_category1"].append(highest_product_category1_name)
        daily_sales_turnover["highest_product_category2"].append(highest_product_category2_name)
        daily_sales_turnover["product_type_name_category1"].append(highest_product_category1_type)
        daily_sales_turnover["product_type_name_category2"].append(highest_product_category2_type)

        # Move to the next day
        current_date += timedelta(days=1)

    # Convert the dictionary to a DataFrame
    result_df = pd.DataFrame(daily_sales_turnover)

    # Now replace the category names in the DataFrame for storing purposes
    result_df.columns = result_df.columns.str.replace(f"{category1}_sales", "footwear_sales")
    result_df.columns = result_df.columns.str.replace(f"{category2}_sales", "home_sales")
    result_df.columns = result_df.columns.str.replace(f"{category1}_turnover", "footwear_turnover")
    result_df.columns = result_df.columns.str.replace(f"{category2}_turnover", "home_turnover")
    result_df.columns = result_df.columns.str.replace("highest_product_category1", "highest_product_footwear")
    result_df.columns = result_df.columns.str.replace("highest_product_category2", "highest_product_home")
    result_df.columns = result_df.columns.str.replace("product_type_name_category1", "product_type_name_footwear")
    result_df.columns = result_df.columns.str.replace("product_type_name_category2", "product_type_name_home")

    return result_df
