import boto3
import logging as logger

from botocore.exceptions import ClientError

s3_client = boto3.client('s3', region_name='us-east-1')


def get_object(bucket_name, object_key):
    try:
        object = s3_client.Object(bucket_name, object_key)
        body = object.get()['Body'].read()
        logger.info("Got object '%s' from bucket '%s'.", object_key, bucket_name)
    except ClientError:
        logger.exception(("Couldn't get object '%s' from bucket '%s'.", object_key, bucket_name))
        raise
    else:
        return body
