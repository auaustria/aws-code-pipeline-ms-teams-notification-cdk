import json
import os
import logging
import urllib.request
import boto3
from urllib.error import URLError, HTTPError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getWebhookUri():
    secret_name = "ms-teams-webhook"
    region_name = os.environ['AWS_REGION']

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret_value = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret_value)
    return secret_dict['uri']

webhookUri = getWebhookUri()

def getMessageColor(state):
    switcher = {
        "STARTED": "good",
        "SUCCEEDED": "good",
        "RESUMED": "good",
        "SUPERSEDED": "warning",
        "FAILED": "attention",
        "CANCELED": "warning",
        "STOPPING": "attention",
        "STOPPED": "attention",
    }
    return switcher.get(state, "default")

def handler(event, context):   
    try:
        factset = [
            {
                "title": "Execution Id",
                "value": f"{event['detail']['execution-id']}"
            }
        ]
        msg = {  
                   "type":"message",  
                   "attachments":[  
                      {  
                         "contentType":"application/vnd.microsoft.card.adaptive",  
                         "content":{  
                            "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",  
                            "type":"AdaptiveCard",  
                            "version":"1.4",  
                            "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text":  f"{event['detail']['state']} : {event['detail']['pipeline']}",
                            "color": f"{getMessageColor(event['detail']['state'])}"
                        },
                        {
                            "type": "FactSet",
                            "facts": factset
                        }
                    ],
                    "actions": [
                            {
                                "type": "Action.OpenUrl",
                                "title": "View in AWS CodePipeline",
                                "url": f"https://{event['region']}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{event['detail']['pipeline']}/view"
                            }
                        ]
                         }  
                      }  
                   ]  
                }
        
        jsonData = json.dumps(msg).encode('utf-8')
        logger.info(f"Request Message: {jsonData}")

        response = urllib.request.urlopen(urllib.request.Request(webhookUri, data=jsonData, headers={"Content-Type": "application/json"}))
        response.read()

    except HTTPError as err:
        logger.info(err)
        logger.error(f"Request failed: {err.code} {err.reason} {err.read().decode('utf-8')}")
    except URLError as err:
        logger.error(f"Server connection failed: {err.reason}")
