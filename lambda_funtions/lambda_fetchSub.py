import boto3
import json


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('subscriptionTable')
    email = event['email']

    try:
        response = table.query(
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={
                ':email': email
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'subscriptions': response['Items']})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error fetching subscriptions'})
        }
