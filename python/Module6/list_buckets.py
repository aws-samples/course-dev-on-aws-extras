import boto3

s3_client = boto3.client('s3', region_name='us-east-1')

response = s3_client.list_buckets()

print('Existing buckets')
for bucket in response['Buckets']:
    print(f' {bucket["Name"]}')