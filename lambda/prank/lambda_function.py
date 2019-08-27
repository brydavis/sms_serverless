from twilio.rest import Client
import json
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    body = parse_qs(event["body"])
    cognito_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    
    print(cognito_id)

    item = dynamodb.Table("users").get_item(
        Key={
            "cognito_id": cognito_id,
        }
    )

    ACCOUNT_SID = item["Item"]["account_sid"]
    AUTH_TOKEN  = item["Item"]["auth_token"]

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to=body["to"], 
            from_= item["Item"]["phone_number"]
        )
    
    return {
        "statusCode": 200,
        "body": call.sid,
        "headers":{
            "Access-Control-Allow-Origin": "*"
        },
    }