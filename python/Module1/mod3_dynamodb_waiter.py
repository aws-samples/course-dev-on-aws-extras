import boto3

def check_table():
    # Create table and wait until it is ready
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # Wait until the table exists.
    dynamodb.meta.client.get_waiter('table_exists').wait(TableName='Notes')

    print("Table exists")
    
check_table()
