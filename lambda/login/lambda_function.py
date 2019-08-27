# SIGN IN
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
import json
from urllib.parse import parse_qs


# These are fake, so please replace
USER_POOL_ID = 'ca-central-1_9ioeruoiG'
CLIENT_ID = 'dhewerm98htu89tac7ioeuroi'
CLIENT_SECRET ='41l3451vlngf5v661ooqr4rk6ljgo0q45iuroiu35uf0070g22c'

client = None

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'),   digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

ERROR = 0
SUCCESS = 1
USER_EXISTS = 2
    
def initiate_auth(username, password):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': get_secret_hash(username),
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password, 
            })
    except client.exceptions.NotAuthorizedException as e:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException as e:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None
    
def lambda_handler(event, context):
    global client
    if client == None:
        client = boto3.client('cognito-idp')
    
    body = parse_qs(event["body"])
    username = body['username'][0]
    password = body['password'][0]

    is_new = False

    is_new = True
    
    resp, msg = initiate_auth(username, password)
    if msg != None:
        return {'status': 'fail', 'msg': msg, "error": True, "success": False, "is_new": is_new}
    id_token = resp['AuthenticationResult']['IdToken']    
    return { 
        "statusCode": 200 , 
        "body": json.dumps({
            "msg": msg, 
            "id_token": id_token
        }),
        "headers":{
            "Access-Control-Allow-Origin": "*"
        }
    }