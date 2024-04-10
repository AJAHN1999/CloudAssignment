import boto3
from urllib.request import urlretrieve
from task1 import *
import os


s3 = boto3.resource('s3')

def downloadImages( imageURL,filename):
    if not os.path.exists('images'):
        os.makedirs('images')
    filepath = os.path.join('images',filename)
    urlretrieve(imageURL, filepath)

def retrieveImages():
    songs = useJSON()
    for id, everySong in enumerate(songs['songs']):
        downloadImages(everySong['img_url'],f'image_{id}.jpg')

if not os.path.exists('images'):
    retrieveImages()

def creates3():
    try:
        s3.create_bucket(Bucket='s3987749images')
        print('Bucket created successfully')
    except Exception as e:
        print(f'Error creating bucket: {e}')
    
    

   
def uploadtos3():
    creates3()
    for file_name in os.listdir('./images/'):
        try:
            file_path= os.path.join('./images/',file_name)
            with open(file_path,'rb') as file:
                s3.Object('s3987749images',file_name).put(Body=file)
        except Exception as e:
            print(f"Error uploading {file_name}: {e}")


uploadtos3()