import json
import os
import logging
import boto3

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
ddb = boto3.resource('dynamodb').Table(os.environ['OHC_TABLE_NAME'])

def main(event, context):

    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - payload: a JSON object containing parameters to pass to the 
                 operation being performed
    '''

    LOG.info('request: {}'.format(json.dumps(event)))

    operation = event['httpMethod']
    if operation is not None:
        return table_operations(event)
    
    return {
        'statusCode': 200,
        'body': 'enter operation',
    }

def table_operations(event):

    body = ''

    if event['httpMethod'] == "GET" and event['path'] == "items":
        body = ddb.scan()
        response = body['Items']
    
    elif event['httpMethod'] == "PUT" and event['path'] == "items":
        item_body = event['item']
        LOG.info(event['item'])
        ddb.put_item(Item = {
            "id" : item_body
        })
        body = f"Put item {item_body}"
        LOG.info(body)
    
    elif event['httpMethod'] == "GET" and event['pathParameters'] == "id":
        LOG.info(event['id'])
        body = ddb.get_item(
            Key = {
                "id": event['id']
            }
        )
        result = body
        LOG.info(result)

    elif event['httpMethod'] == 'DELETE' and event['pathParameters'] == "id":
        body = ddb.delete_item(
            Key={
                "id": event['id']
            }
        )
        body = f"Deleted item {event['id']}"

    body = json.dumps(body)

    return {
    'statusCode': 200,
    'body': body,
    'headers': 'Content-Type',
    }

