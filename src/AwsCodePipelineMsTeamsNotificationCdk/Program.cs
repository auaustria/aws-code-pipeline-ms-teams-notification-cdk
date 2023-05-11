using Amazon.CDK;

namespace AwsCodePipelineMsTeamsNotificationCdk
{
    sealed class Program
    {
        public static void Main(string[] args)
        {
            var app = new App();
            var account = System.Environment.GetEnvironmentVariable("CDK_DEFAULT_ACCOUNT");
            var region = System.Environment.GetEnvironmentVariable("CDK_DEFAULT_REGION");

            new AwsCodePipelineMsTeamsNotificationCdkStack(app, "AwsCodePipelineMsTeamsNotificationCdkStack", new StackProps
            {
                // If you don't specify 'env', this stack will be environment-agnostic.
                // Account/Region-dependent features and context lookups will not work,
                // but a single synthesized template can be deployed anywhere.

                // Uncomment the next block to specialize this stack for the AWS Account
                // and Region that are implied by the current CLI configuration.
                /*
                Env = new Amazon.CDK.Environment
                {
                    Account = System.Environment.GetEnvironmentVariable("CDK_DEFAULT_ACCOUNT"),
                    Region = System.Environment.GetEnvironmentVariable("CDK_DEFAULT_REGION"),
                }
                */

                Env = new Amazon.CDK.Environment
                {
                    Account = account,
                    Region = region,
                },

                StackName = $"codepipeline-notification-stack",
                CrossRegionReferences = true,
                Description = "Application Stack for AWS CodePipeline to MS Teams notification using CDK"


                // For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
            });
            app.Synth();
        }
    }
}
