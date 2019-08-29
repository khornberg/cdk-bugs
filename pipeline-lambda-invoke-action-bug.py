from aws_cdk import core
from aws_cdk.aws_codepipeline import Artifact
from aws_cdk.aws_codepipeline import Pipeline
from aws_cdk.aws_codepipeline import StageProps
from aws_cdk.aws_codepipeline_actions import GitHubSourceAction
from aws_cdk.aws_codepipeline_actions import LambdaInvokeAction
from aws_cdk.aws_iam import Role
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_s3 import Bucket


class Stack(core.Stack):
    def __init__(self, scope):
        super().__init__(scope, "bug")
        bucket = Bucket.from_bucket_name(
            self, "artifacts", core.Fn.import_value("CodeArtifactsBucket")
        )
        pipeline_role = Role.from_role_arn(
            self, "pipeline", core.Fn.import_value("CodePipelineRole")
        )
        pipeline = Pipeline(
            self,
            "Pipeline",
            artifact_bucket=bucket,
            role=pipeline_role,
            stages=[
                StageProps(
                    stage_name="Source",
                    actions=[
                        GitHubSourceAction(
                            action_name="Source",
                            run_order=1,
                            oauth_token=core.SecretValue("something"),
                            output=Artifact(artifact_name="SourceArtifact"),
                            owner="me",
                            repo="repo",
                            branch="master",
                        )
                    ],
                )
            ],
        )
        pipeline.add_stage(
            stage_name="Fails",
            actions=[
                LambdaInvokeAction(
                    action_name="LambdaInvokeAction",
                    run_order=1,
                    lambda_=Function.from_function_arn(
                        self, "function", core.Fn.import_value("SomeFunction")
                    ),
                )
            ],
        )


app = core.App()
Stack(app)
application = app.synth()
