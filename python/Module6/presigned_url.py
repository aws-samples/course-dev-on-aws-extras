import boto3
import os

bucket = os.environ['MY_BUCKET']

url = boto3.client('s3', region_name='us-east-1').generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': bucket, 'Key': 'airports.csv'},
    ExpiresIn=3600
)

print(url)