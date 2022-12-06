import boto3
import botocore

s3_client = boto3.client('s3', region_name='us-east-1')

def verify_bucket_name(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        raise SystemExit('This bucket has already been created')
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print('Existing bucket not found, please proceed')
        if error_code == 403:
            raise SystemExit('This bucket is already owned by another AWS account')

verify_bucket_name("morgan")