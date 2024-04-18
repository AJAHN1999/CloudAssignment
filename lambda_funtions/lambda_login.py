import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('login')

    email = event['email']
    password = event['password']

    response = table.get_item(
        Key={
            'email':email
        }
    )
    if 'Item' in response:
        user = response['Item']
        if user['password'] == password:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'LoggedIn successful', 'user': user})
            }
        else:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'WrongPassword'})
            }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'UserNotFound'})
        }