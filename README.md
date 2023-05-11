# MS Teams Notifications from AWS CodePipeline.

**A quick attempt to build a MS Teams notification stack

This project is a uses the following:
- Webhook Connector in Microsoft teams
- AWS Lambda in python to format and send adaptive card message to the webhook
- CDK code to generate AWS resources for the stack
- Reads a secret value in AWS Secrets manager for the Webhook URI. 

Get a webhook uri by Configuring the Webhook connector in a microsoft teams channel.
To set the URI of the webhook, create a secret named ms-teams-webhook (or change secret_name variable in the python code for a custom secret name)
At this point you can synth/deploy the cdk. It prefers to use an aws profile so use
```cdk deploy --profile [your_profile_name]```
