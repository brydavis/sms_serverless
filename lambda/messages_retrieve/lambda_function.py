# GET MESSAGES
import boto3
import json
from urllib.parse import parse_qs
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    # body = parse_qs(event["body"])
    cognito_id = event["requestContext"]["authorizer"]["claims"]["sub"]

    user = dynamodb.Table("users").get_item(
        Key={
            "cognito_id": cognito_id,
        }
    )["Item"]

    messages = dynamodb.Table("messages").scan(
        FilterExpression=Attr("account_sid").eq(user["account_sid"])
    )["Items"]

    return { 
        "statusCode": 200,
        "body": json.dumps(messages),  
        "headers":{
            "Access-Control-Allow-Origin": "*"
        },  
    }