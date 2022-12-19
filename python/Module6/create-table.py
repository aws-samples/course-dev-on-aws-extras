import boto3

dynamodb = boto3.resource('dynamodb')
tableName = "Notes2"

def create_table():
    print("Creating table...")
    table = dynamodb.create_table(
        TableName=tableName,
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

    print("Table has been created!")

def update_table():
    table = dynamodb.Table(tableName)
    table = table.update(
        ProvisionedThroughput={
            'ReadCapacityUnits': 7,
            'WriteCapacityUnits': 7
        })

    while True:
        response = table.meta.client.describe_table(
            TableName=tableName
        )
        print(response['Table']['TableStatus'])
        if response['Table']['TableStatus'] == 'ACTIVE':
            break

    print("Table has been updated!")


def delete_table():
    response = dynamodb.meta.client.delete_table(
        TableName=tableName
    )

    print("Table has been deleted!")


def list_tables():
    response = dynamodb.meta.client.list_tables(
        Limit=10
    )
    print(response)

create_table()
update_table()
delete_table()
list_tables()