import boto3

s3_client = boto3.client('s3', region_name='us-east-1')

r = s3_client.select_object_content(
    Bucket='morgansamples3bucket',
    Key='airports.csv',
    ExpressionType='SQL',
    Expression="select * from s3object s where s.\"iso_country\" like '%US%'",
    InputSerialization={'CSV': {"FileHeaderInfo": "Use"}},
    OutputSerialization={'CSV': {}},
)

for event in r['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)
