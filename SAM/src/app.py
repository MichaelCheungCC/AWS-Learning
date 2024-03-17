
import boto3
import json
import os

dynamo = boto3.client('dynamodb')
table_name = os.environ['TABLE_NAME']


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'GET': lambda dynamo, x: dynamo.get_item(TableName=table_name, Key=x),
        'POST': lambda dynamo, x: dynamo.put_item(TableName=table_name, Item=x),
        'DELETE': lambda dynamo, x: dynamo.delete_item(TableName=table_name, Key=x)
    }

    # Easier syntax without declaring the type of value
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table(TableName)
    # table.put_item({"fruitName" : 'banana'})

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(
            event['body'])
        payload = {'ID': {'S': str(payload['ID'])}} if operation == 'GET' else json.loads(payload['Item'])
        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
