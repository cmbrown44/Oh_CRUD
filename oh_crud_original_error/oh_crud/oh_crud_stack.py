import aws_cdk
from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as ddb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,        
    # aws_sqs as sqs,
)
# from aws_cdk.aws_apigateway import LambdaIntegration as apihttp
from constructs import Construct

class OhCrudStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:

        # The code that defines your stack goes here

        ohc_table = ddb.Table(self, "OhCrudTable", partition_key=ddb.Attribute(name="id", type=ddb.AttributeType.STRING))

        ohc_function = _lambda.Function(self, "OhCrudFunction",
        handler="handler.main",
        code=_lambda.Code.from_asset("./lambda"),
        runtime=_lambda.Runtime.PYTHON_3_9,
        environment={
                'OHC_TABLE_NAME': ohc_table.table_name,
            })

         # create role that grants permissions to upload logs to CloudWatch
        assert ohc_function.role is not None
        ohc_function.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )

        ohc_table.grant_read_write_data(ohc_function)

        ohc_api = apigw.LambdaRestApi(self, "OhCApi",
        handler=ohc_function,
        proxy=False)

        items = ohc_api.root.add_resource("items")
        items.add_method("GET") # GET /items
        items.add_method("PUT") # PUT /items

        item_id = items.add_resource("{id}")
        item_id.add_method("GET") # GET /items/{id}
        item_id.add_method("DELETE") # DELETE /items/{id}