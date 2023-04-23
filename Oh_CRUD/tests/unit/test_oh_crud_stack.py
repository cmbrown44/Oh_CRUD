import aws_cdk as core
import aws_cdk.assertions as assertions

from oh_crud.oh_crud_stack import OhCrudStack

# example tests. To run these tests, uncomment this file along with the example
# resource in oh_crud/oh_crud_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = OhCrudStack(app, "oh-crud")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
