import json
import urllib.parse
import boto3
import uuid
import pyarrow.csv as pv
import pyarrow.parquet as pq


def csv_to_parquet(source_path):
    table = pv.read_csv(source_path)
    pq.write_table(table, source_path.replace('csv', 'parquet'))

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # Event based on s3 event notification of lambda trigger
    #bucket = event['Records'][0]['s3']['bucket']['name']
    #key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    # Event based on eventbridge > step function
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']

    tmpkey = key.replace('/', '_')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    upload_path = download_path.replace('csv', 'parquet')
    
    try:
        s3.download_file(bucket, key, download_path)
        csv_to_parquet(download_path)
        s3.upload_file(upload_path, "s3-event-notification-destination", key.replace('csv', 'parquet'))
        return {
            'statusCode': 200,
            'body': 'CSV copied as parquet successfully.'
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }   