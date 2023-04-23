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

    if event['httpMethod'] == "GET" & event['path'] == "items":
        body = ddb.scan()
        body = body['Items']
    
    elif event['routeKey'] == "PUT/items":
        requestJSON = json.loads(event['body'])
        LOG.info(requestJSON['item'])
        ddb.put_item(item = {
            "id" : {
                "s" : requestJSON['id']
            }
        })
        body = f"Put item {requestJSON['i']}"
    
    elif event['routeKey'] == 'GET/items/{id}':
        body = ddb.get_item(
            Key = {
                id: event['pathParameters']['id']
            }
        )
        body = body['item']

    elif event['routeKey'] == 'DELETE/items/{id}':
        body = ddb.delete_item(
            Key={
                id: event['pathParameters']['id']
            }
        )
        body = f"Deleted item {event['pathParameters']['id']}"

    body = json.dumps(body)

    return {
    'statusCode': 200,
    'body': body,
    'headers': 'Content-Type',
    }