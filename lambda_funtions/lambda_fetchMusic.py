import boto3
import json


def lambda_handler(event, context):
    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    music_table = dynamodb.Table('music')
    
    # Parse incoming music details from the Lambda event
    music_details=event
    print(music_details)
    
    # Generate the query, attribute values, and names
    query, expression_attribute_values, expression_attribute_names = create_query(music_details)
    print("Query:", query)
    print(f'{expression_attribute_names} are expression_attribute_names')
    print(expression_attribute_values)
    
    if query:
        scan_params = {
            "FilterExpression": query,
            "ExpressionAttributeValues": expression_attribute_values,
        }
        # Only add ExpressionAttributeNames if it's not empty and needed
        if expression_attribute_names:
            scan_params["ExpressionAttributeNames"] = expression_attribute_names
        # Execute the scan operation
        response = music_table.scan(**scan_params)
        music_list = response['Items']  # List of dictionaries
        # Add images to each music item
        music_list_with_images = add_images(music_list)

    # Return the processed music list
    return {
        'statusCode': 200,
        'body': json.dumps({'musicList': music_list_with_images})
    }

def create_query(music_details):
    filter_expressions = []
    expression_attribute_values = {}
    expression_attribute_names = {}
    year = music_details.get('year', None)
    title = music_details.get('title', None)
    artist = music_details.get('artist', None)
    print(year)
    print(title)
    print(artist)
    if artist!=None:
        filter_expressions.append("artist = :artist")
        expression_attribute_values[':artist'] = music_details['artist']
    if year!=None:
        filter_expressions.append("#yr = :year")
        expression_attribute_values[':year'] = music_details['year']
        expression_attribute_names['#yr'] = 'year'
    if title!=None:
        filter_expressions.append("title = :title")
        expression_attribute_values[':title'] = music_details['title']

    query = " AND ".join(filter_expressions)
    return query, expression_attribute_values, expression_attribute_names

def add_images(music_list):
    s3 = boto3.client('s3')
    bucket_name = 's3987749images'  # Specify your bucket name
    for song in music_list:
        object_key = f"{song['artist']}.jpg"
        img_url = generate_presigned_url(s3, bucket_name, object_key)
        if img_url:
            song['image_url'] = img_url
    return music_list


def generate_presigned_url(s3_client, bucket_name, object_key, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={
                                                        'Bucket': bucket_name,
                                                        'Key': object_key
                                                    },
                                                    ExpiresIn=expiration)
        return response
    except Exception as e:
        print(e)
        return None