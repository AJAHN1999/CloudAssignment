import boto3 
from flask import Flask, jsonify

dynamodb = boto3.resource('dynamodb',region_name="us-east-1") 
loginTable = dynamodb.Table('login')



def login(request):
    data = request.form
    response = validateLogin(data)
    return response

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
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Incorrect password'})
    else:
        return jsonify({'message': 'User not found'})
    

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
