from twilio.rest import Client
import json
import boto3
from urllib.parse import parse_qs

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    body = parse_qs(event["body"])
    cognito_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    
    item = dynamodb.Table("users").get_item(
        Key={
            "cognito_id": cognito_id, # body["cognito_id"]} ## UPDATE TO AUTHORIZER
        }
    )

    ACCOUNT_SID = item["Item"]["account_sid"]
    AUTH_TOKEN  = item["Item"]["auth_token"]

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    message = client.messages.create(
        to=body["to"], 
        from_= item["Item"]["phone_number"], ## body["from"], # not safe; hackable, curry that shit
        body=body["message"])
    

    return {
        "statusCode": 200,
        "body": message.sid,
        "headers":{
            "Access-Control-Allow-Origin": "*"
        },
    }