import boto3

# import logging
# boto3.set_stream_logger('botocore', logging.DEBUG)

dynamo = boto3.client("dynamodb")
tables = dynamo.list_tables();

for table_name in tables['TableNames']:
    print(table_name)


s3 = boto3.client("s3")
#  using an zero filled file created on the command line with: truncate -s 10m 10meg.dat
s3.upload_file("10meg.dat", 'rrs-sydney', '10meg.dat')


print("Uploaded!")