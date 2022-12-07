import boto3
import os

bucket = os.environ['MY_BUCKET']

s3_client = boto3.client('s3', region_name='us-east-1')

paginator = s3_client.get_paginator('list_objects')
page_iterator = paginator.paginate(Bucket=bucket,
                                   PaginationConfig={'MaxItems': 10})

for page in page_iterator:
    print(page['Contents'])