# SIGN UP
import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
from urllib.parse import parse_qs

# These are fake, so please replace
USER_POOL_ID = 'ca-central-1_9ioeruoiG'
CLIENT_ID = 'dhewerm98htu89tac7ioeuroi'
CLIENT_SECRET ='41l3451vlngf5v661ooqr4rk6ljgo0q45iuroiu35uf0070g22c'

client = None
dynamodb = boto3.resource("dynamodb")

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(
        str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'),   
        digestmod=hashlib.sha256
    ).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

ERROR = 0
SUCCESS = 1
USER_EXISTS = 2
    

def sign_up(username, password):
    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password
        )
        return {
            "statusCode": SUCCESS,
            "cognito_id": resp["UserSub"],
        }
    # except client.exceptions.UsernameExistsException as e:
    #     return {
    #         "statusCode": USER_EXISTS,
    #         "error": str(e),
    #     }
    except Exception as e:
        return {
            "statusCode": ERROR,
            "error": str(e),
        }

    
def lambda_handler(event, context):
    global client
    if client == None:
        client = boto3.client('cognito-idp')
    # body = parse_qs(event["body"])
    
    username = body['username'][0]
    password = body['password'][0]

    signed_up = sign_up(username, password)
    # if signed_up["statusCode"] == ERROR:
    #     return {'status': 'fail', 'msg': 'failed to sign up'}
    # if signed_up["statusCode"] == SUCCESS:
        # print ('Success in  sign up')
        # dynamodb.Table("users").put_item(
        #     Item={
        #         "cognito_id": signed_up["cognito_id"], #  user["requestContext"]["authorizer"]["claims"]["sub"],
        #         "username": username, #  user["requestContext"]["authorizer"]["claims"]["email"],
        #     }
        # )

    return { 
        "statusCode": 200, 
        "body": "OK",
        "headers":{
            "Access-Control-Allow-Origin": "*"
        }
    }

