import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine

# Data quality report definition
df_dqreport = pd.DataFrame(columns=["FileName", "Record Count", "Duplicates Count", "null counts", "inserted rows"])

# DONE Read data from CSV into dataframe for further analysis and action
df = pd.read_csv('data\customers_raw.csv')
cust_csv_rows = len(df)
cust_csv_null_summary = pd.DataFrame({
    "Column Name": df.columns,
    "Null Count": df.isnull().sum().values
})
cust_csv_null_summary = cust_csv_null_summary[cust_csv_null_summary['Null Count']>0]

# DONE Drop duplicates
df = df.drop_duplicates()
cust_csv_dup_count = cust_csv_rows - len(df)

print("here")

df_dqreport.loc[len(df)] = ['Customers_csv', cust_csv_rows,cust_csv_dup_count,cust_csv_null_summary,20]
print("data quality report")
print(df_dqreport)

# DONE update the email ID to customercare@fleximart.com. This is so that the 
# rows_with_nan_in_email = df[df['email'].isna()]
df.loc[df['email'].isnull(),'email'] = (df.loc[df['email'].isnull(),'email'].astype(str)+df['customer_id']+'@flexmart.com').str[3:]
# print(df)

# DONE Standardize phone formats. 
# Strategy: Remove all values beyond 10 digits from the right, and prefix them all with '+91-'
df.loc[df['phone'].str.len() > 10, 'phone'] = df.loc[df['phone'].str.len() > 10, 'phone'].str[-10:]
df['phone'] = "+91-"+df['phone']
# print(df)

# DONE Standardize date format
df['registration_date'] = pd.to_datetime(df['registration_date'],format='mixed')
# print (df)

# CustomerID to be transformed to integer 
df['customer_id'] = df['customer_id'].str[1:]
df['customer_id'] = df['customer_id'].astype(int)

# Read and Prepare Products data for upload
# ----------------------------------------------

# read the products data
df_p = pd.read_csv('data\products_raw.csv')

# product_id values to be transformed to integer 
df_p['product_id'] = df_p['product_id'].str[1:]
df_p['product_id'] = df_p['product_id'].astype(int)

#product_name remove extra paces
df_p['product_name'] = df_p['product_name'].str.split().str.join(' ')

# category values to be in title case
df_p['category'] = df_p['category'].str.title()

# Where price is null, provide a value as 99,999,999.99 which is the max size by column definition
df_p.loc[df_p['price'].isnull(),'price'] = 99999999.99

# Where stock_qty is NaN, defaulting to 0.0 in alignment with the create script
df_p['stock_quantity'].fillna(0.0, inplace=True)

####### This completes preparing Products data for upload 

# Read and Prepare Sales data for upload
# ----------------------------------------------

# read the sales data
df_s = pd.read_csv('data\sales_raw.csv')

# remove duplicates
df_s = df_s.drop_duplicates()

# customer_id missing records: drop those records as there is no way we can guess who the customer is
df_s = df_s.dropna(subset='customer_id')

# fix date format
df_s['transaction_date'] = pd.to_datetime(df_s['transaction_date'],format='mixed')

# fix missing product ID. Here I miss the Vlookup of excel. 
# Ideally I would like to refer to the unit_price in sales, and fetch corresponding product ID from products table
# T008 has a product with unit price 1299. By visual inspection I can take it is P008
# T025 has a product with unit price 1999. By visual inspection I can take it is P005 
df_s.loc[(df_s['transaction_id']=="T008"),'product_id'] = 'P008'
df_s.loc[(df_s['transaction_id']=="T025"),'product_id'] = 'P005'

# update T, C and Ps to make them all int
df_s['product_id'] = df_s['product_id'].str[1:]
df_s['product_id'] = df_s['product_id'].astype(int)

df_s['transaction_id'] = df_s['transaction_id'].str[1:]
df_s['transaction_id'] = df_s['transaction_id'].astype(int)

df_s['customer_id'] = df_s['customer_id'].str[1:]
df_s['customer_id'] = df_s['customer_id'].astype(int)

# create total_amount 
df_s['total_amount'] = df_s['quantity'] * df_s['unit_price']

df_s = df_s.rename(columns={'transaction_id': 'order_id'})
df_s = df_s.rename(columns={'transaction_date': 'order_date'})


# create 2 dataframes to load into orders and order_items
df_o = df_s.loc[:,['order_id','customer_id','order_date','total_amount','status']].copy()
print (df_o)
df_ito = df_s.loc[:,['order_id','product_id','quantity','unit_price','total_amount']].copy()
df_ito = df_ito.rename(columns={'total_amount':'subtotal'})
print(df_ito)

# Database connection details
DB_HOST = '127.0.0.1'  # 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'admin'
DB_NAME = 'fleximart'

db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(db_url)
conn = engine.raw_connection()
cursor = conn.cursor()

try:
    
    df.to_sql(
        name = 'customers',
        con = engine,
        if_exists='append',
        index=False
    )
    conn.commit()
    print("DataFrame customers successfully loaded into MySQL.")

    df_p.to_sql(
        name = 'products',
        con = engine,
        if_exists='append',
        index=False
    )
    conn.commit()
    print("DataFrame products successfully loaded into MySQL.")

    df_o.to_sql(
        name = 'orders',
        con = engine,
        if_exists='append',
        index=False

    )
    conn.commit()
    print("DataFrame Orders successfully loaded into MySQL.")

    df_ito.to_sql(        
        name = 'order_items',
        con = engine,
        if_exists='append',
        index=False

    )
    conn.commit()
    print("DataFrame Order items successfully loaded into MySQL.")
    

finally:
    cursor.close()
    conn.close()
