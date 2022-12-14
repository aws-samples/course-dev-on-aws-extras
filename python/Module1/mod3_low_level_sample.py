import boto3

# Return type: dict / additional API calls needed to get objects
def list_objects():
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket='rrs-apps')
    for content in response['Contents']:
        print(content['Key'], content['LastModified'])

list_objects()