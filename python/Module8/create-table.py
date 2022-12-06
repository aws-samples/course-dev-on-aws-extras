import boto3

dynamodb = boto3.resource('dynamodb')

def create_table():
    table = dynamodb.create_table(
        TableName='Notes',
        KeySchema=[
            {
                'AttributeName': 'UserId',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'NoteId',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'UserId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'NoteId',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()

    print(table.item_count)

def update_table():
    table = dynamodb.Table('Notes')
    table = table.update(
        ProvisionedThroughput={
            'ReadCapacityUnits': 7,
            'WriteCapacityUnits': 7
        })

def delete_table():
    response = dynamodb.meta.client.delete_table(
        TableName='Notes'
    )

def list_tables():
    response = dynamodb.meta.client.list_tables(
        Limit=10
    )
    print(response)

create_table()
update_table()
delete_table()
list_tables()