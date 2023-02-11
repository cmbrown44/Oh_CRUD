import json
import os

import boto3

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['OHC_TABLE_NAME'])
_lambda = boto3.client('lambda')


def main(event, context):
    print('request: {}'.format(json.dumps(event)))
    print("Hello World")