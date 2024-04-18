import boto3
import json

def lambda_handler(event, context):
    # Extract data from the event
    email = event['email']  # Assume email is passed directly or via an authorizer
    song_info = event['songInfo']

    # Add subscription to the DynamoDB table
    response = add_to_subscribed_music(email, song_info)
    
    # Return success or failure response
    if response:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Subscription added successfully'})
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to add subscription'})
        }

def add_to_subscribed_music(email, song_info):
    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    subscription_table = dynamodb.Table('subscriptions')

    try:
        response = subscription_table.put_item(
            Item={
                'email': email,
                'music_title': song_info.get('song_title'),
                'image': song_info.get('song_imgURL'),
                'yearr': song_info.get('song_year'),  
                'artist': song_info.get('song_artist')
            }
        )
        return response['ResponseMetadata']['HTTPStatusCode'] == 200
    except Exception as e:
        print(e)
        return False