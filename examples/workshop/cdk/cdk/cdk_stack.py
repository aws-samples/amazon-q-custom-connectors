import os
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput as StackOutput,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_lambda as lambda_,
    aws_iam as iam,
)
from aws_cdk.aws_ecr_assets import DockerImageAsset, Platform
from constructs import Construct
import cdk_nag as nag

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Custom data source resources
        vpc = ec2.Vpc(self, "WorkshopVpc", max_azs=2)

        nag.NagSuppressions.add_resource_suppressions(
            vpc,
            [{
                "id": "AwsSolutions-VPC7",
                "reason": "This is a VPC for the workshop and is meant to be destroyed after the workshop is complete."
            }]
        )

        ecs_cluster = ecs.Cluster(self, "WorkshopEcsCluster", vpc=vpc)

        nag.NagSuppressions.add_resource_suppressions(
            ecs_cluster,
            [{
                "id": "AwsSolutions-ECS4",
                "reason": "This is an ECS for the workshop and is meant to be destroyed after the workshop is complete."
            }]
        )

        container_image = DockerImageAsset(self, "WorkshopDataSourceImage", 
            directory="../datasource",
            platform=Platform.LINUX_AMD64
        )

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "WorkshopService",
            cluster=ecs_cluster,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_docker_image_asset(container_image),
                container_name="qbus-workshop-datasource",
                container_port=5000,
            ),
            public_load_balancer=True
        )

        nag.NagSuppressions.add_resource_suppressions(
            fargate_service,
            [{
                "id": "AwsSolutions-ELB2",
                "reason": "This is an ELB for the workshop and is meant to be destroyed after the workshop is complete."
            },{
                "id": "AwsSolutions-EC23",
                "reason": "This is an ELB for the workshop and is meant to be destroyed after the workshop is complete."
            },{
                "id": "AwsSolutions-IAM5",
                "reason": "This is an Task IAM role/policy for the workshop and is meant to be destroyed after the workshop is complete."
            }],
            True
        )

        # Connector Lambda function
        connector_fn = lambda_.Function(self, "Connector",
            code=lambda_.Code.from_asset("../connector"),
            handler="connector.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            memory_size=1024,
            timeout=Duration.seconds(900),
            environment={
                "Q_INDEX_ID": "",
                "Q_DATASOURCE_ID": "",
                "Q_APPLICATION_ID": "",
                "OAUTH2_CLIENT_ID": "clientid",
                "OAUTH2_SECRET": "secret",
                "OAUTH2_TOKEN_URL": f'http://{fargate_service.load_balancer.load_balancer_dns_name}/oauth/token',
                "GENERIC_DATASOURCE_URL": f'http://{fargate_service.load_balancer.load_balancer_dns_name}'
            }
        )

        connector_fn.add_to_role_policy(iam.PolicyStatement(
            actions=[
                "qbusiness:StartDataSourceSyncJob",
                "qbusiness:BatchPutDocument",
                "qbusiness:StopDataSourceSyncJob",
            ],
            effect=iam.Effect.ALLOW,
            resources=[
                f"*",
            ]
        ))
        nag.NagSuppressions.add_resource_suppressions(
            connector_fn,
            [{
                "id": "AwsSolutions-IAM4",
                "reason": "This is an Lambda IAM role/policy for the workshop and is meant to be destroyed after the workshop is complete."
            },{
                "id": "AwsSolutions-IAM5",
                "reason": "This is an Lambda IAM role/policy for the workshop and is meant to be destroyed after the workshop is complete."
            }],
            True
        )

        # CFN outputs
        StackOutput(self, "ConnectorArn", value=connector_fn.function_arn)
        StackOutput(self, "ConnectorName", value=connector_fn.function_name)
        StackOutput(self, "ImageUri", value=container_image.image_uri)
        StackOutput(self, "StackId", value=self.stack_id)