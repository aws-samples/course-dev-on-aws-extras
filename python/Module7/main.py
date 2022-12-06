"DynamoDB Sample app"
import csv
import json
import re
import boto3
from geopy import distance

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

# import logging
# boto3.set_stream_logger('botocore.endpoint', logging.DEBUG)

dynamodb = boto3.resource('dynamodb')
dynamo_client = boto3.client('dynamodb')

# you can launch dynamo-local in a docker container:
# docker run -d -p 8000:8000 amazon/dynamodb-local
# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
# dynamo_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")

state_codes = {'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC', 'Federated States Of Micronesia': 'FM', 'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Marshall Islands': 'MH', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Palau': 'PW', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}

def create_table():
    "Create the DynamoDB table."
    table = dynamodb.create_table(
        TableName='CityPopulation',
        KeySchema=[
            {
                'AttributeName': 'StateCode',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'CityName',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'StateCode',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'CityName',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'AirportCode',
                'AttributeType': 'S'
            }
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'StateCode-AirportCode-localindex',
                'KeySchema': [
                    {
                        'AttributeName': 'StateCode',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'AirportCode',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                }
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'AirportCode-globalindex',
                'KeySchema': [
                    {
                        'AttributeName': 'AirportCode',
                        'KeyType': 'HASH'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 2,
                    'WriteCapacityUnits': 2
                }
            },
        ]
    )
    print(table)
    input("Press Enter to continue...")


def scan_query():
    "Compare scans and queries"
    print("Scanning table - CityName = Portland")
    table_scan = dynamo_client.scan(
        TableName='CityPopulation',
        ReturnConsumedCapacity='TOTAL',
        ScanFilter={
            'CityName' : {
                'AttributeValueList' : [{ 'S' : 'Portland'}],
                'ComparisonOperator' : 'EQ'
            }
        },
        ConsistentRead=False
    )
    print_cities(table_scan)
    print()

    print("Querying table - StateCode = OR")
    table_query = dynamo_client.query(
        TableName='CityPopulation',
        KeyConditions={
            'StateCode': {
                'AttributeValueList': [{ "S" : 'OR'}],
                'ComparisonOperator' : 'EQ'
            }
        },
        ReturnConsumedCapacity='TOTAL',
        ConsistentRead=False
    )
    print_cities(table_query)
    print()

    print("Querying local index - StateCode = OR, AirportCode = KPDX")
    table_query = dynamo_client.query(
        TableName='CityPopulation',
        IndexName="StateCode-AirportCode-localindex",
        KeyConditions={
            'StateCode': {
                'AttributeValueList': [{ "S" : 'OR'}],
                'ComparisonOperator' : 'EQ'
            },
            'AirportCode': {
                'AttributeValueList': [{ "S" : 'KPDX'}],
                'ComparisonOperator' : 'EQ'
            }
        },
        ReturnConsumedCapacity='TOTAL',
        ConsistentRead=False
    )
    print_cities(table_query)
    print()

    print("Querying global index - AirportCode = KPDX")
    table_query = dynamo_client.query(
        TableName='CityPopulation',
        IndexName="AirportCode-globalindex",
        KeyConditions={
            'AirportCode': {
                'AttributeValueList': [{ "S" : 'KPDX'}],
                'ComparisonOperator' : 'EQ'
            }
        },
        ReturnConsumedCapacity='TOTAL'
    )
    print_cities(table_query)
    print()

    input("Press Enter to continue...")

def print_cities(items):
    print("Cities: ")
    for i in items["Items"]:
        print(f' - {i["CityName"]["S"]}, {i["StateCode"]["S"]} {i["AirportCode"]["S"]} ')
    print("Consumed capacity: ", items["ConsumedCapacity"]["CapacityUnits"])


def partiql_query():
    "query with PartiQL"
    print("PartiQL query - find city Portland")
    # To ensure that a SELECT statement does not result in a full table scan, the WHERE clause condition must specify a partition key.
    # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.select.html
    execute_query = dynamo_client.execute_statement(
        Statement="SELECT * FROM CityPopulation where CityName = ?",
        Parameters=[{
            'S': 'Portland',
        }],
        ReturnConsumedCapacity='TOTAL',
        ConsistentRead=False
    )
    print("Item count: ", len(execute_query["Items"]))
    if "ConsumedCapacity" in execute_query:
        print("Consumed capacity: ", execute_query["ConsumedCapacity"])
    print()

    print("PartiQL query - use global index")
    execute_query = dynamo_client.execute_statement(
        Statement='SELECT * FROM "CityPopulation"."AirportCode-globalindex" where AirportCode = ?',
        Parameters=[{
            'S': 'KPDX',
        }],
        ReturnConsumedCapacity='TOTAL'
    )
    print("Item count: ", len(execute_query["Items"]))
    if "ConsumedCapacity" in execute_query:
        print("Consumed capacity: ", execute_query["ConsumedCapacity"])
    print()

    input("Press Enter to continue...")


def load_table():
    "populate the dynamo table"
    with open('airport-codes.csv', encoding='utf-8') as airports_csv:
        reader = csv.DictReader(airports_csv)
        airports = [ a for a in reader if a["type"] == "large_airport" ]

    with open('us-cities-top-1k.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        cities = list(reader)

    print("Finding the closest airport")
    for row in cities:
        lat, lng = float(row["lat"]), float(row["lon"])
        sort_airports = sorted(
            airports,
            key=lambda d, pos=(lat,lng): distance.distance(
                pos,
                (float(d["coordinates"].split(", ")[0]), float(d["coordinates"].split(" ")[1]))
                ).km
        )
        row["airport_code"] = sort_airports[0]['ident']
        print(row["City"], row["airport_code"])

    print("Saving cities to Dynamo")
    for row in cities:
        city = row["City"]
        population = row["Population"]
        state = state_codes[row["State"]]
        airport_code = row["airport_code"]
        print(city, state, population, airport_code)

        response = dynamo_client.put_item(
            TableName='CityPopulation',
            Item={
                'StateCode': { "S" : state },
                'CityName': { "S" : city },
                'Population': { "N":  population },
                'AirportCode' : { "S" : airport_code }
            }
        )
        print(f'Response: {response["ResponseMetadata"]}')
    input("Press Enter to continue...")


menu = ConsoleMenu("DynamoDB", "Playground")
create_item = FunctionItem("Create table", create_table)
load_item = FunctionItem("Load the table", load_table)
scan_item = FunctionItem("Scan/query the table and indexes", scan_query)
partiql_item = FunctionItem("PartiQL queries", partiql_query)

menu.append_item(create_item)
menu.append_item(load_item)
menu.append_item(scan_item)
menu.append_item(partiql_item)
menu.show()
