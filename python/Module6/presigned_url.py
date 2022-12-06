import boto3

url = boto3.client('s3', region_name='us-east-1').generate_presigned_url(
    ClientMethod='get_object',
    Params={'Bucket': 'morgansamples3bucket', 'Key': 'airports.csv'},
    ExpiresIn=3600
)

print(url)