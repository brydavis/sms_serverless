# UPDATE USER
import boto3
import json
from urllib.parse import urlencode, parse_qs

dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    body = parse_qs(event["body"])
    update_expression = "SET " + ", ".join([k+" = :"+k for k,v in body.items() if k != "cognito_id"]) 
    expression_attribute_values = { ":"+k: v[0] for k,v in body.items() if k != "cognito_id" }
    cognito_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    
    dynamodb.Table("users").update_item(
        Key={
            "cognito_id": cognito_id,
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
    return { 
        "statusCode": 200,
        "body": "OK", 
        "headers":{
            "Access-Control-Allow-Origin": "*"
        },   
    }