import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Function to filter and count the product data by date
def filter_sweater_by_date(input_file, start_date_str, date_column='t_dat', product_type='Sweater'):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Ensure the date column exists and is in datetime format
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column])

        # Convert start date string to a timestamp
        start_date = pd.Timestamp(start_date_str)
        end_date = start_date + pd.Timedelta(days=10)

        # Filter the DataFrame for the specified product type in the given date range
        filtered_df = df[
            (df['product_type_name'] == product_type) &
            (df[date_column] >= start_date) &
            (df[date_column] <= end_date)
        ]

        # Group by date and count occurrences of the product type
        datewise_count = filtered_df.groupby(date_column)['product_type_name'].count()

        # Convert the index (which is a timestamp) to string for JSON serialization
        datewise_count = datewise_count.reset_index()
        datewise_count[date_column] = datewise_count[date_column].apply(lambda x: x.isoformat())

        # Return the date-wise count as a dictionary
        return datewise_count.to_dict(orient='records')
    else:
        raise ValueError(f"'{date_column}' column not found in the file. Please check the CSV file.")

# Flask route to trigger the function and return results as JSON
@app.route('/filter-sweater', methods=['GET'])
def get_sweater_data():
    # Get input parameters from the query string
    input_file = request.args.get('input_file', 'filtered_data.csv')  # Default file
    start_date_str = request.args.get('start_date', '2018-10-11')  # Default start date

    try:
        # Call the function with the provided parameters
        result = filter_sweater_by_date(input_file, start_date_str)
        # Return the result as JSON
        return jsonify(result)
    except ValueError as e:
        # Return an error message as JSON if there's an exception
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
