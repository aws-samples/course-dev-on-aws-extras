import boto3
import os

s3_client = boto3.client('s3', region_name='us-east-1')

bucket = os.environ['MY_BUCKET']


def get_object(bucket_name, object_key):
    with open('airportsdownload.csv', 'wb') as f:
        s3_client.download_fileobj(bucket_name, object_key, f)




def head_object(bucket_name, object_key):
    response = s3_client.head_object(
        Bucket=bucket_name,
        Key=object_key,
    )

    print(response)


head_object(bucket, 'airports.csv')
get_object(bucket, 'airports.csv')
