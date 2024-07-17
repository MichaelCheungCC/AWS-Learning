import boto3
import csv
import json
import urllib.parse


def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    dynamodb_resource = boto3.resource('dynamodb')

    # Event based on s3 event notification of lambda trigger
    #bucket = event['Records'][0]['s3']['bucket']['name']
    #key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    # Event based on eventbridge > step function
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    
    try:
        # Read the CSV file from S3 and store as JSON
        response = s3_client.get_object(Bucket=bucket, Key=key)
        csv_content = response['Body'].read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_content)
        items = list(csv_reader)
    
        # Insert items into DynamoDB
        table_name = 'f_sales'
        table = dynamodb_resource.Table(table_name)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
    
        return {
            'statusCode': 200,
            'body': 'CSV into DynamoDB successfully.'
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }