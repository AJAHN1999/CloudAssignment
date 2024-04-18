import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('login')
    
    username = event['username']
    email = event['email']
    password = event['password']
    
    try:
        Validationresponse = table.get_item( #validateUser method
        Key={
            'email':email
        }
    )
        if 'Item' not in Validationresponse:
            response = table.put_item(
                Item={
                'username': username,
                'email': email,
                'password': password
                }
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'User added successfully'})
                }
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'message': 'Failed to add user'})
                }
        else:
            return {
                    'statusCode': 500,
                    'body': json.dumps({'message': 'Failed to add user,user already exists'})
                }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error accessing database'})
        }