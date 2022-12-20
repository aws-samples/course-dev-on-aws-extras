import boto3
import os
import timeit

bucket_name = os.environ["MY_BUCKET"]
client = boto3.client("s3")

def getStringCount(search_string, s3_operation = "get_object"):
    # list the contents of the s3 bucket shakespeare prefix
    response = client.list_objects_v2(
        Bucket=bucket_name,
        Prefix='shakespeare/'
    )

    total_count = 0
    # loop thru all the keys returned by the list operation
    for content in response["Contents"]:
        key = content["Key"]
        print(f"Scanning {key}")

        if s3_operation == "get_object":
            response = client.get_object(Bucket=bucket_name,
                                Key=key)
            key_body = response['Body'].read()
            total_count += key_body.decode('utf8').upper().count(search_string.upper())

        elif s3_operation == "select_object_content":
            reponse = client.select_object_content(
                Bucket=bucket_name,
                Key=key,
                ExpressionType='SQL',
                Expression=f"select _1 from s3object where upper(_1) like '%{search_string.upper()}%'",
                InputSerialization={
                    'CSV': {'FileHeaderInfo': 'NONE'},
                    'CompressionType': 'NONE'
                },
                OutputSerialization={'CSV': {}}
            )
            for event in reponse['Payload']:
                if 'Records' in event:
                    total_count += event['Records']['Payload'].decode('utf-8').upper().count(search_string.upper())

    # we have a total count!
    print(f"Counted {total_count}")


print(timeit.timeit(stmt='getStringCount("queen", "get_object")', globals=globals(), number=1))
print(timeit.timeit(stmt='getStringCount("queen", "select_object_content")', globals=globals(), number=1))