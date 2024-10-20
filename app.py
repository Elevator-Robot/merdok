from typing import cast, Any
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_bedrock as bedrock,
    aws_iam as iam,
)
from constructs import Construct
from aws_cdk.aws_iam import IPrincipal

class MerdokStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

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

        bedrock.CfnAgent(self, "BedrockAgent",
            agent_name="MerdokAgent",
            description="Merdok Agent",
            action_groups=[
                bedrock.CfnAgent.AgentActionGroupProperty(
                    action_group_name="bedrock-dice-roller",
                    action_group_state="ENABLED",
                    description="Default action group",
                )
            ],
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

app = cdk.App()
MerdokStack(app, "MerdokStack")

app.synth()
