import boto3
import os

s3_client = boto3.client('s3', region_name='us-east-1')

bucket = os.environ['MY_BUCKET']

paginator = s3_client.get_paginator('list_objects')
page_iterator = paginator.paginate(Bucket=bucket,
                                   PaginationConfig={'PageSize': 2})

for page in page_iterator:
    json_data = page['Contents']
    for item in json_data:
        print(item['Key'])