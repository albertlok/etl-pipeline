import pandas as pd
import psycopg2.extras as p
from utils.db import WarehouseConnection
from utils.sfl_config import get_warehouse_creds

# Query in SQL for data insertion into table
def _get_user_data_insert_query():
    return """
    INSERT INTO info.userinfo (
        id,
        first_name,
        last_name,
        email,
        gender,
        ip_address
    )
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

# Read data from CSV, transform some columns, and return as list
def get_user_data(filename='DE Data.csv'):
    data_df = pd.read_csv('./' + filename)      # Can replace file path with desired path on local system
    data_df['id'] = data_df['id'].apply(int)    # Cast id column into integers
    data_df['first_name'] = data_df['first_name'].str.capitalize()  # Names already appear to be capitalized, but just to be sure
    data_df['last_name'] = data_df['last_name'].str.capitalize()    # Names already appear to be capitalized, but just to be sure
    data_df['email'] = data_df['email'].str.lower()     # Lowercase emails for easier potential parsing
    data_df['gender'] = data_df['gender'].str.lower()   # Lowercase gender for easier potential parsing
    return data_df.values.tolist()

# Function to get data from CSV and insert each user into warehouse
def load_user_data():
    user_data = get_user_data()
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        p.execute_batch(curr, _get_user_data_insert_query(), user_data)


if __name__ == "__main__":
    load_user_data()
