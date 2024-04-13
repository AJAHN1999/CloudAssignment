import boto3
dynamoDB = boto3.resource('dynamodb', region_name="us-east-1")

def createSubscriptionsTable():
    try:
        subscriptionsTable = dynamoDB.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            },
            {
                'AttributeName':'music_title',
                'AttributeType':'S'
            }
        ],
        TableName='subscriptions',
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            },
            {
                'AttributeName':'music_title',
                'KeyType':'RANGE'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
        )
    except:
        print(" subscriptions table already created")

createSubscriptionsTable()