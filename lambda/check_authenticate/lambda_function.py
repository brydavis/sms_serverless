# GET USER
import boto3
# import json


def lambda_handler(event, context):
    try:
        cognito_id = event["requestContext"]["authorizer"]["claims"]["sub"]
        return { 
            "statusCode": 200,
            "body": cognito_id,
            "headers":{
                "Access-Control-Allow-Origin": "*"
            },   
        }    

    except Exception as e:
        return { 
            "statusCode": 404,
            "body": str(type(e).__name__),
            "headers":{
                "Access-Control-Allow-Origin": "*"
            },   
        }
        
  

    