import boto3
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Notes')


def write_note():
    table.put_item(
        Item={
            'UserId': 'StudentX',
            'NoteId': 70,
            'Note': 'I love python',
            'Favorite': 'Yes',
        }
    )

def get_note():
    response = table.get_item(
        Key={
            'UserId': 'StudentA',
            'NoteId': 78
        }
    )
    item = response['Item']
    print(item)

def delete_note():
    table.delete_item(
        Key={
            'UserId': 'StudentX',
            'NoteId': '70'
        }
    )

def query_notes_by_user_id():
    response = table.query(
        KeyConditionExpression=Key('UserId').eq('StudentA')
    )
    items = response['Items']
    print(items)

def query_favorite_notes():
    response = table.scan(
        FilterExpression=Attr('Favorite').eq('Yes')
    )
    items = response['Items']
    print(items)

write_note()
get_note()
delete_note()
query_notes_by_user_id()
query_favorite_notes()