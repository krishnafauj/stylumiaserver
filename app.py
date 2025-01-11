from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from catvscat import calculate_daily_sales_and_turnover  # Import the function from catvscat.py
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
CORS(app)

data_store = {"example": "This is a test value"}

# PostgreSQL connection details
db_config = {
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "VP2pugIsJF1U",
    "host": "ep-shy-brook-a8ryyvuf.eastus2.azure.neon.tech",
    "port": "5432"
}

# Function to insert data into the PostgreSQL database
def insert_data_to_db(data):
    try:
        # Establish connection
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'sales_data_1'
            );
        """)
        table_exists = cursor.fetchone()[0]

        # If the table doesn't exist, create it
        if not table_exists:
            create_table_query = """
                CREATE TABLE sales_data_1 (
                    id SERIAL PRIMARY KEY,
                    date DATE,
                    footwear_sales INT,
                    home_sales INT,
                    footwear_turnover DOUBLE PRECISION,
                    home_turnover DOUBLE PRECISION,
                    highest_product_footwear VARCHAR(255),
                    highest_product_home VARCHAR(255),
                    product_type_name_footwear VARCHAR(255),
                    product_type_name_home VARCHAR(255)
                );
            """
            cursor.execute(create_table_query)
            conn.commit()
            print("Table sales_data_1 created successfully.")

        # SQL query to insert the data into sales_data_1 table
        insert_query = """
            INSERT INTO sales_data_1 (
                date, 
                footwear_sales, 
                home_sales, 
                footwear_turnover, 
                home_turnover, 
                highest_product_footwear, 
                highest_product_home, 
                product_type_name_footwear, 
                product_type_name_home
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Insert each record into the database
        for row in data:
            cursor.execute(insert_query, (
                row['date'], 
                row['footwear_sales'], 
                row['home_sales'], 
                row['footwear_turnover'], 
                row['home_turnover'], 
                row['highest_product_footwear'], 
                row['highest_product_home'], 
                row['product_type_name_footwear'], 
                row['product_type_name_home']
            ))

        # Commit the transaction
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully!")

    except Exception as e:
        print("Error inserting data into the database:", e)

# GET endpoint
@app.route('/api/get', methods=['GET'])
def get_value():
    key = request.args.get('key')  # Retrieve 'key' parameter from the query string
    if key in data_store:
        return jsonify({"key": key, "value": data_store[key]})
    else:
        return jsonify({"error": "Key not found"}), 404

@app.route('/compare', methods=['POST'])
def compare_data():
    try:
        # Get the JSON payload from the request
        data = request.json  
        print("Received data:", data)  # Print the received data for debugging

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract the necessary values from the received JSON
        final_date = data.get("date")
        days = int(data.get("duration", 0))
        category1 = data.get("category1")
        category2 = data.get("category2")

        if not all([final_date, days, category1, category2]):
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Call the function to calculate daily sales and turnover
        result_df = calculate_daily_sales_and_turnover(final_date, days, category1, category2)
        
        # Convert the result DataFrame to JSON (you can adjust the data as needed)
        result_json = result_df.to_dict(orient='records')
        
        # Print the result to check
        print(result_json)
        
        # Insert the result into the database
        insert_data_to_db(result_json)

        # Return the JSON response
        return jsonify({
            "message": "Data processed successfully",
            "data": result_json
        })
    
    except Exception as e:
        print("Error:", e)  # Log the error in case of failure
        return jsonify({"error": str(e)}), 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

