import boto3 
from flask import Flask, jsonify
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb',region_name="us-east-1") 
loginTable = dynamodb.Table('login')
musicTable = dynamodb.Table('music')
s3_resource = boto3.resource('s3')
bucket_name = 's3987749images'
s3_client = boto3.client('s3')






def login(request):
    data = request.form
    response, user = validateLogin(data)
    return response, user

def validateUser(registrationData):
    # username = registrationData.get('username')
    email = registrationData.get('email')
    # password = registrationData.get('password')
    response = getItem(loginTable,email)
    return response
    

def getItem(tableName,variable):
    return tableName.get_item(
        Key={
            'email':variable
        }
    )
    
def validateLogin(data):
    email = data.get('email')
    password = data.get('password')
    
    response = getItem(loginTable,email)
    if 'Item' in response:
        user = response['Item']
        if user['password']==password:
            return jsonify({'message': 'LoggedIn successful'}), user
        else:
            return jsonify({'message': 'WrongPassword'}), None
    else:
        return jsonify({'message': 'UserNotFound'}), None
    

def addUser(registrationData):
    username = registrationData.get('username')
    email = registrationData.get('email')
    password = registrationData.get('password')
    response = loginTable.put_item(
        Item ={
            'username':username,
            'email':email,
            'password':password
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def createQuery(musicDetails):
    #scan attributes for music queries
    filter_expressions=[]
    expression_attribute_values={}
    expression_attribute_names= {}
    if musicDetails.get('artist'):
        filter_expressions.append("artist=:artist")
        expression_attribute_values[':artist']=musicDetails.get('artist')
    if musicDetails.get('year'):
        filter_expressions.append("#yr=:year")
        expression_attribute_values[':year']=musicDetails.get('year')
        expression_attribute_names['#yr'] = 'year' 
    if musicDetails.get('title'):
        filter_expressions.append("title=:title")
        expression_attribute_values[':title']=musicDetails.get('title')
    
    #combining all filter expressions
    query = " AND ".join(filter_expressions)
    return query ,expression_attribute_values, expression_attribute_names

    
#helps generate presigned URLs to grant access to private images in the s3 bucket- s3987749images
def genPresignedUrl(bucket_name,object_key,expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket':bucket_name,'Key':object_key},ExpiresIn = expiration)
    except ClientError as e:
        return None
    return response


def addImages(musicList):
    for everySong in musicList:
        object_key = everySong['artist']+'.jpg'
        imgURL = genPresignedUrl(bucket_name,object_key)
        if(imgURL!= None):
            everySong['image_url']=imgURL
    return musicList



def fetchMusic(musicDetails):
    query, expression_attribute_values, expression_attribute_names = createQuery(musicDetails)
    if query:
        scan_params = {
            "FilterExpression": query,
            "ExpressionAttributeValues": expression_attribute_values,
        }
        # Only add ExpressionAttributeNames if it's not empty and needed
        if expression_attribute_names:
            scan_params["ExpressionAttributeNames"] = expression_attribute_names
        
        response = musicTable.scan(**scan_params)
        musicList = response['Items'] #list of dictionaries
        return addImages(musicList)  #adds corresponding images by generating presigned URLs to the recieved query results
    else:
        return None






        
    
    