import aws_cdk as core
import aws_cdk.assertions as assertions

from merdok.merdok_stack import MerdokStack

# example tests. To run these tests, uncomment this file along with the example
# resource in merdok/merdok_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MerdokStack(app, "merdok")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
