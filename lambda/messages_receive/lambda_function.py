# RECEIVE SMS
import boto3
from urllib.parse import urlencode, parse_qs

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    message = parse_qs(event["body"])

    dynamodb.Table("messages").put_item(
        Item={
            "message_sid": message["MessageSid"][0], 
            "account_sid": message["AccountSid"][0], 
            "to": message["To"][0], 
            "from": message["From"][0], 
            "body": " ".join(message["Body"]), 
        }
    )

    return {
        "statusCode": 200,
        "body": "OK",
        "headers":{
            "Access-Control-Allow-Origin": "*"
        },
    }