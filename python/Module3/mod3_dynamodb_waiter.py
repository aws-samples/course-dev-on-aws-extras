import boto3

def create_table():
    # Create table and wait until it is ready
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName='Notes4',
        KeySchema=[
            {
                'AttributeName': 'NoteID',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'NoteAuthor',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'NoteID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'NoteAuthor',
                'AttributeType': 'S'
            },
    
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='Notes')
    # Print out some data about the table.
    print(table.item_count)
    
create_table()
