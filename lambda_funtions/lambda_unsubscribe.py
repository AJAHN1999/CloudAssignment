import boto3
import json

def lambda_handler(event, context):
    # Extract data from the event
    email = event['email']  # Assume email is passed directly or via an authorizer
    song_info = event['songInfo']

    # Remove subscription from the DynamoDB table
    response = remove_from_sub_music(email, song_info)
    
    # Return success or failure response
    if response:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Subscription removed successfully'})
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to remove subscription'})
        }

def remove_from_sub_music(email, song_info):
    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    subscription_table = dynamodb.Table('subscriptions')

    try:
        response = subscription_table.delete_item(
            Key={
                'email': email,
                'music_title': song_info.get('song_title')
            }
        )
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except Exception as e:
        print(e)
        return False
