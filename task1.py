import boto3
from create_users import *
import json




dynamoDB = boto3.resource('dynamodb', region_name="us-east-1")

def create_login_table():
    try:
        login = dynamoDB.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'email',
                'AttributeType': 'S'
            }
        ],
        TableName='login',
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
        )
    except:
        print(" login table already created")

# print("Table status:", login.table_status)

def add_users():
    loginTable =dynamoDB.Table('login')

    for i in range(0,10):
        loginTable.put_item(
        Item={
            'email': studentEmail[i],
            'username': studentName[i],
            'password': passwords[i],
        }
    )
        
def createMusicTable():
    try:
        musicTable = dynamoDB.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'artist',
                'AttributeType': 'S'
            },
            {
                'AttributeName':'title',
                'AttributeType':'S'
            }
        ],
        TableName='music',
        KeySchema=[
            {
                'AttributeName': 'artist',
                'KeyType': 'HASH'
            },
            {
                'AttributeName':'title',
                'KeyType':'RANGE'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
        )
    except:
        print(" music table already created")


def useJSON():
    songsFile = open('a1.json')
    songs = json.load(songsFile)
    return songs


def addMusic():
    songs = useJSON()
    musicTable =dynamoDB.Table('music')
    for everySong in songs['songs']:
        musicTable.put_item(
            Item={
                'artist': everySong['artist'],
                'title': everySong['title'], 
                'year': everySong['year'], 
                'web_url': everySong['web_url'], 
                'img_url': everySong['img_url']
            }
        )



#addMusic()
#createMusicTable()










