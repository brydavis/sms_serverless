# CONFIRM SIGN UP
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

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
    
def lambda_handler(event, context):
    global client
    if client == None:
        client = boto3.client('cognito-idp')
    try:
        body = parse_qs(event["body"])
        username = body['username'][0]
        # # password = body['password'][0]
        code = body['code'][0]
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            ConfirmationCode=code,
            ForceAliasCreation=False,
        )
    except client.exceptions.UserNotFoundException as e:
        return response
    except client.exceptions.CodeMismatchException as e:
        return {"error": True, "success": False, "message": "Invalid Verification code"}
    except client.exceptions.NotAuthorizedException as e:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}
    return {
        "statusCode": 200,
        "body": "OK",
        "headers":{
            "Access-Control-Allow-Origin": "*"
        },
    }