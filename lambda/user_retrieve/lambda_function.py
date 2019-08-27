# GET USER
import boto3
import json

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    user = dynamodb.Table("users").get_item(
        Key={
            "cognito_id": event["requestContext"]["authorizer"]["claims"]["sub"],
        }
    )
    return { 
        "statusCode": 200,
        "body": json.dumps(user["Item"]),
        "headers":{
            "Access-Control-Allow-Origin": "*"
        },   
    }