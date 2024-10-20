from typing import cast, Any
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_bedrock as bedrock,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_appsync as appsync,
)
from constructs import Construct
from aws_cdk.aws_iam import IPrincipal
from aws_cdk.aws_lambda_event_sources import DynamoEventSource

class MerdokStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table for Chat Sessions
        chat_table = dynamodb.Table(self, "ChatTable",
            partition_key=dynamodb.Attribute(
                name="chatSessionId",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            stream=dynamodb.StreamViewType.NEW_IMAGE
        )

        # IAM Role for Bedrock Agent
        bedrock_agent_service_role = iam.Role(self, "BedrockAgentServiceRole",
            assumed_by=cast(IPrincipal, iam.ServicePrincipal("bedrock.amazonaws.com"))
        )

        bedrock_agent_service_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "bedrock:*",
            ],
            resources=[
                "*"
            ]
        ))

        # Bedrock Agent Definition
        bedrock.CfnAgent(self, "BedrockAgent",
            agent_name="MerdokAgent",
            description="Merdok Agent",
            foundation_model=bedrock.FoundationModel.from_foundation_model_id(
                self, "FoundationModel",
                bedrock.FoundationModelIdentifier.ANTHROPIC_CLAUDE_3_5_SONNET_20240620_V1_0,
            ).model_id,
            instruction=(
                "You are the Dungeon Master, guiding adventurers on their expeditions. Be clever and clear in your instructions. "
                "Create engaging and challenging scenarios for the adventurers. Provide detailed descriptions of the environment, "
                "characters, and events. Ensure the campaign is immersive and enjoyable. Keep track of the adventurers' progress "
                "and adapt the story as needed. Your role is to facilitate an exciting and memorable campaign."
            ),
            auto_prepare=True,
            skip_resource_in_use_check_on_delete=True,
            idle_session_ttl_in_seconds=300,
            agent_resource_role_arn=bedrock_agent_service_role.role_arn,
        )

        # Lambda Function to Interact with Bedrock
        bedrock_lambda = _lambda.Function(self, "BedrockLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="bedrock_handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "CHAT_TABLE_NAME": chat_table.table_name
            }
        )

        # Grant DynamoDB Permissions to Lambda
        chat_table.grant_read_write_data(bedrock_lambda)

        # Add DynamoDB Stream as Event Source for Lambda
        bedrock_lambda.add_event_source(
            DynamoEventSource(chat_table,
                starting_position=_lambda.StartingPosition.LATEST,
            )
        )

        # AppSync API Definition
        api = appsync.CfnGraphQLApi(self, "MerdokApi",
            name="MerdokApi",
            authentication_type="AMAZON_COGNITO_USER_POOLS",
            xray_enabled=True,
            user_pool_config=appsync.CfnGraphQLApi.UserPoolConfigProperty(
                user_pool_id="us-east-1_jq7L9L7CH",
                aws_region="us-east-1",
                default_action="ALLOW"
            )
        )

        # Output the value of api.ref
        cdk.CfnOutput(self, "GraphQLApiId",
            value=api.attr_api_id,
            description="The ID of the AppSync GraphQL API"
        )
        # GraphQL Schema
        appsync.CfnGraphQLSchema(self, "MerdokSchema",
            api_id=api.attr_api_id,
            definition=open("schema.graphql").read()
        )

        # Chat Table Data Source for AppSync
        chat_table_data_source = appsync.CfnDataSource(self, "ChatTableDataSource",
            api_id=api.attr_api_id,
            name="ChatTableDataSource",
            type="AMAZON_DYNAMODB",
            dynamo_db_config=appsync.CfnDataSource.DynamoDBConfigProperty(
                table_name=chat_table.table_name,
                aws_region=self.region
            ),
            service_role_arn=bedrock_agent_service_role.role_arn
        )

        list_messages_resolver = appsync.CfnResolver(self, "ListMessagesResolver",
            api_id=api.attr_api_id,
            type_name="Query",
            field_name="listMessages",
            data_source_name=chat_table_data_source.name,
            request_mapping_template=open("resolvers/listMessagesRequest.vtl").read(),
            response_mapping_template=open("resolvers/listMessagesResponse.vtl").read(),
        )

        list_messages_resolver.node.add_dependency(chat_table_data_source)

        # Lambda Data Source for AppSync (already exists)
        lambda_data_source = appsync.CfnDataSource(self, "LambdaDataSource",
            api_id=api.attr_api_id,
            name="LambdaDataSource",
            type="AWS_LAMBDA",
            lambda_config=appsync.CfnDataSource.LambdaConfigProperty(
                lambda_function_arn=bedrock_lambda.function_arn
            ),
            service_role_arn=bedrock_agent_service_role.role_arn
        )

        # Resolver for sendMessageToChat mutation
        send_message_resolver = appsync.CfnResolver(self, "SendMessageToChatResolver",
            api_id=api.attr_api_id,
            type_name="Mutation",
            field_name="sendMessageToChat",
            data_source_name=lambda_data_source.name,
            request_mapping_template=open("resolvers/sendMessageToChatRequest.vtl").read(),
            response_mapping_template=open("resolvers/sendMessageToChatResponse.vtl").read(),
        )

        # Make resolver dependent on the Lambda data source
        send_message_resolver.node.add_dependency(lambda_data_source)

app = cdk.App()
MerdokStack(app, "MerdokStack")

app.synth()
