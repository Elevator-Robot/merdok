from aws_cdk import RemovalPolicy, Stack
from aws_cdk.aws_appsync import (
    CfnGraphQLSchema,
    CfnGraphQLApi,
    CfnApiKey,
    CfnDataSource,
    CfnResolver,
)
from aws_cdk.aws_dynamodb import (
    Table,
    Attribute,
    AttributeType,
    StreamViewType,
    BillingMode,
)
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from constructs import Construct
from typing import cast, Any
import aws_cdk as cdk
from aws_cdk import (
    aws_bedrock as bedrock,
    aws_iam as iam,
    aws_appsync as appsync,
)
from aws_cdk.aws_iam import IPrincipal


class MerdokStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ############################################
        #### DynamoDB Table
        ############################################

        # Create the DynamoDB table for messages
        messages_table = Table(
            self,
            "MessagesTable",
            partition_key=Attribute(name="conversationId", type=AttributeType.STRING),
            sort_key=Attribute(name="id", type=AttributeType.STRING),
            billing_mode=BillingMode.PAY_PER_REQUEST,
            stream=StreamViewType.NEW_IMAGE,
            removal_policy=RemovalPolicy.DESTROY,  # For development only
        )
        messages_table.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        # Create the AppSync API
        chat_api = CfnGraphQLApi(
            self, "ChatApi", name="chat-api", authentication_type="API_KEY"
        )

        # Create API Key
        CfnApiKey(self, "ChatApiKey", api_id=chat_api.attr_api_id)

        # Define schema
        api_schema = CfnGraphQLSchema(
            self,
            "ChatSchema",
            api_id=chat_api.attr_api_id,
            definition="""\
                type Message {
                    id: ID!
                    conversationId: String!
                    content: String!
                    sender: String!
                    timestamp: String!
                }
                type Query {
                    getConversation(conversationId: String!): [Message]
                    listConversations: [Message]
                }
                input SendMessageInput {
                    conversationId: String!
                    content: String!
                    sender: String!
                }
                type Mutation {
                    sendMessage(input: SendMessageInput!): Message
                }
                type Schema {
                    query: Query
                    mutation: Mutation
                }""",
        )

        # Create IAM role for DynamoDB access
        dynamodb_role = Role(
            self,
            "ChatDynamoDBRole",
            assumed_by=ServicePrincipal("appsync.amazonaws.com"),
        )

        dynamodb_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
        )

        ############################################
        #### AppSync Resolvers
        ############################################

        # Create DynamoDB data source
        messages_ds = CfnDataSource(
            self,
            "MessagesDataSource",
            api_id=chat_api.attr_api_id,
            name="MessagesDynamoDataSource",
            type="AMAZON_DYNAMODB",
            dynamo_db_config=CfnDataSource.DynamoDBConfigProperty(
                table_name=messages_table.table_name, aws_region=self.region
            ),
            service_role_arn=dynamodb_role.role_arn,
        )

        # Create resolvers
        get_conversation_resolver = CfnResolver(
            self,
            "GetConversationQueryResolver",
            api_id=chat_api.attr_api_id,
            type_name="Query",
            field_name="getConversation",
            data_source_name=messages_ds.attr_name,
            request_mapping_template="""\
            {
                "version": "2017-02-28",
                "operation": "Query",
                "query": {
                    "expression": "conversationId = :conversationId",
                    "expressionValues": {
                        ":conversationId": $util.dynamodb.toDynamoDBJson($ctx.args.conversationId)
                    }
                }
            }""",
            response_mapping_template="$util.toJson($ctx.result.items)",
        )
        get_conversation_resolver.add_depends_on(api_schema)
        get_conversation_resolver.add_depends_on(messages_ds)

        list_conversations_resolver = CfnResolver(
            self,
            "ListConversationsQueryResolver",
            api_id=chat_api.attr_api_id,
            type_name="Query",
            field_name="listConversations",
            data_source_name=messages_ds.attr_name,
            request_mapping_template="""\
            {
                "version": "2017-02-28",
                "operation": "Scan"
            }""",
            response_mapping_template="$util.toJson($ctx.result.items)",
        )
        list_conversations_resolver.add_depends_on(api_schema)
        list_conversations_resolver.add_depends_on(messages_ds)

        send_message_resolver = CfnResolver(
            self,
            "SendMessageMutationResolver",
            api_id=chat_api.attr_api_id,
            type_name="Mutation",
            field_name="sendMessage",
            data_source_name=messages_ds.attr_name,
            request_mapping_template="""\
            {
                "version": "2017-02-28",
                "operation": "PutItem",
                "key": {
                    "conversationId": $util.dynamodb.toDynamoDBJson($ctx.args.input.conversationId),
                    "id": $util.dynamodb.toDynamoDBJson($util.autoId())
                },
                "attributeValues": {
                    "content": $util.dynamodb.toDynamoDBJson($ctx.args.input.content),
                    "sender": $util.dynamodb.toDynamoDBJson($ctx.args.input.sender),
                    "timestamp": $util.dynamodb.toDynamoDBJson($util.time.nowISO8601())
                }
            }""",
            response_mapping_template="$util.toJson($ctx.result)",
        )
        send_message_resolver.add_depends_on(api_schema)
        send_message_resolver.add_depends_on(messages_ds)


        ############################################
        ### Lambda Function
        ############################################
        lambda_role = iam.Role(
            self,
            "DynamoStreamLambdaRole",
            assumed_by=ServicePrincipal("lambda.amazonaws.com"),
        )

        lambda_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:*",
                ],
                resources=["*"],
            )
        )

        dynamo_stream_lambda = cdk.aws_lambda.Function(
            self,
            "DynamoStreamLambda",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=cdk.aws_lambda.Code.from_asset("lambda"),
            environment={"TABLE_NAME": messages_table.table_name},
        )

        # event source mapping
        dynamo_stream_lambda.add_event_source(
            cdk.aws_lambda_event_sources.DynamoEventSource(
                messages_table,
                starting_position=cdk.aws_lambda.StartingPosition.TRIM_HORIZON,
                batch_size=1,
                bisect_batch_on_error=True,
                retry_attempts=5,
                filters=[{'eventName': ['INSERT']}]
            )
        )

        ############################################
        ### Bedrock Agent
        ############################################

        # IAM Role for Bedrock Agent
        bedrock_agent_service_role = iam.Role(
            self,
            "BedrockAgentServiceRole",
            assumed_by=cast(IPrincipal, iam.ServicePrincipal("bedrock.amazonaws.com")),
        )

        bedrock_agent_service_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:*",
                ],
                resources=["*"],
            )
        )

        # Bedrock Agent Definition
        bedrock.CfnAgent(
            self,
            "BedrockAgent",
            agent_name="MerdokAgent",
            description="Merdok Agent",
            foundation_model=bedrock.FoundationModel.from_foundation_model_id(
                self,
                "FoundationModel",
                bedrock.FoundationModelIdentifier.ANTHROPIC_CLAUDE_3_SONNET_20240229_V1_0,
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

        # Output the value of api.ref
        cdk.CfnOutput(
            self,
            "GraphQLApiId",
            value=chat_api.attr_api_id,
            description="The ID of the AppSync GraphQL API",
        )


app = cdk.App()
MerdokStack(app, "MerdokStack")

app.synth()
