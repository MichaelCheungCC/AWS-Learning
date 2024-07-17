import pandas as pd
import random
import datetime
import os
import boto3
from botocore.exceptions import ClientError


today = datetime.datetime.today()-datetime.timedelta(days=random.randint(1, 30))
year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")
today_yyyymmdd = today.strftime("%Y%m%d")
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

path = f"./Lambda/Data/Year={year}/Month={month}"
file_name = path + f"/{today_yyyymmdd}_sales.csv"
object_name = f"Sales/Year={year}/Month={month}/{today_yyyymmdd}_sales.csv"

num_rows = random.randint(10, 100)  # Number of rows to generate

sales_data = {
    'date_id': [today_yyyymmdd for _ in range(1, num_rows)],
    'order_id': range(1, num_rows),
    'store_id': [random.randint(1, 50) for _ in range(1, num_rows)],
    'customer_id': [random.randint(1, num_rows) for _ in range(1, num_rows)],
    'product_id': [random.randint(1, 200) for _ in range(1, num_rows)],
    'quantity': [random.randint(1, 10) for _ in range(1, num_rows)],
    'file_generation_time': [current_datetime for _ in range(1, num_rows)]
}

df = pd.DataFrame(sales_data)

if not os.path.isdir(path):
    os.makedirs(path)

if not os.path.isfile(file_name):
    df.to_csv(file_name, index=False)
s3_client = boto3.client('s3')

try:
    s3_client.upload_file(file_name, "s3-event-notification-source", object_name)
except:
    raise ClientError