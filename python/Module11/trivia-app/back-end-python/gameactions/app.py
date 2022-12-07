"Backend for the trivia game"
import json
import os
import random
import uuid

import boto3
import yaml
from botocore.exceptions import ClientError

DYNAMODB = boto3.resource('dynamodb')
TABLE = DYNAMODB.Table(os.getenv('TABLE_NAME'))
MANAGEMENT = boto3.client('apigatewaymanagementapi', endpoint_url=os.getenv('APIGW_ENDPOINT'))
STEPFUNCTIONS = boto3.client('stepfunctions')
COLORS = ("AliceBlue,AntiqueWhite,Aqua,Aquamarine,Azure,Beige,Bisque,Black,BlanchedAlmond,Blue,"
"BlueViolet,Brown,BurlyWood,CadetBlue,Chartreuse,Chocolate,Coral,CornflowerBlue,Cornsilk,Crimson,"
"Cyan,DarkBlue,DarkCyan,DarkGoldenrod,DarkGray,DarkGreen,DarkKhaki,DarkMagenta,DarkOliveGreen,"
"DarkOrange,DarkOrchid,DarkRed,DarkSalmon,DarkSeaGreen,DarkSlateBlue,DarkSlateGray,DarkTurquoise,"
"DarkViolet,DeepPink,DeepSkyBlue,DimGray,DodgerBlue,FireBrick,FloralWhite,ForestGreen,Fuchsia,"
"Gainsboro,GhostWhite,Gold,Goldenrod,Gray,Green,GreenYellow,Honeydew,HotPink,IndianRed,Indigo,"
"Ivory,Khaki,Lavender,LavenderBlush,LawnGreen,LemonChiffon,LightBlue,LightCora,LightCyan,"
"LightGoldenrodYellow,LightGreen,LightGrey,LightPink,LightSalmon,LightSeaGreen,LightSkyBlue,"
"LightSlateGray,LightSteelBlu,LightYellow,Lime,LimeGreen,Linen,Magenta,Maroon,MediumAquamarine,"
"MediumBlue,MediumOrchid,MediumPurple,MediumSeaGreen,MediumSlateBlue,MediumSpringGreen,"
"MediumTurquoise,MediumVioletRed,MidnightBlue,MintCream,MistyRose,Moccasin,NavajoWhite,Navy,"
"OldLace,Olive,OliveDrab,Orange,OrangeRed,Orchid,PaleGoldenrod,PaleGreen,PaleTurquoise,"
"PaleVioletRed,PapayaWhip,PeachPuff,Peru,Pink,Plum,PowderBlue,Purple,Red,RosyBrown,RoyalBlue,"
"SaddleBrown,Salmon,SandyBrown,SeaGreen,Seashell,Sienna,Silver,SkyBlue,SlateBlue,SlateGray,Snow,"
"SpringGreen,SteelBlue,Tan,Teal,Thistle,Tomato,Turquoise,Violet,Wheat,White,WhiteSmoke,Yellow,"
"YellowGreen").split(",")
WAIT_SECONDS = 5

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(SCRIPT_PATH, "all-questions.yaml"), 'r', encoding="utf-8") as stream:
    QUESTIONS = yaml.safe_load(stream)

def get_random_player_name():
    "Generate a random player name"
    return random.choice(COLORS)

def get_body_param(event, param):
    "Load JSON body content and get the value of a property"
    body = json.loads(event["body"])
    value = body[param]
    return value

def get_players(game_id):
    "Query dynamo for a list of game players"
    connections = TABLE.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("gameId").eq(game_id)
    )
    return [{
        "connectionId" : p["connectionId"],
        "playerName": p["playerName"],
        "score": int(p["score"])
        } for p in connections["Items"]]

def send_broadcast(connections, data):
    "Post out websocket messages to a list of connection ids"
    for connection in connections:
        try:
            if "action" in data and data["action"] == "playerlist":
                # we need to insert "currentPlayer" into player list broadcasts
                for player in data["players"]:
                    player["currentPlayer"] = (connection==player["connectionId"])

            MANAGEMENT.post_to_connection(
                Data=json.dumps(data),
                ConnectionId=connection
            )
        except ClientError as error:
            if error.response['Error']['Code'] == 'GoneException':
                print("Missing connection ", connection)

def trivia_newgame(event, _):
    "Lambda function to intitate a new game"
    game_id = uuid.uuid4().hex

    # write the connection and game id into the dynamo table
    connection_id = event["requestContext"]["connectionId"]
    player_name = get_random_player_name()
    connection = {
        "gameId": game_id,
        "connectionId": connection_id,
        "playerName": player_name,
        "score": 0
    }
    TABLE.put_item(Item=connection)

    # send game created
    MANAGEMENT.post_to_connection(
        Data=json.dumps({"action": "gamecreated", "gameId": game_id}),
        ConnectionId=connection_id
    )

    # send player list of single player
    MANAGEMENT.post_to_connection(
        Data=json.dumps({"action": "playerlist", "players": [
            {
                "connectionId" : connection_id,
                "currentPlayer" : True,
                "playerName": player_name,
                "score": 0
            }
        ]}),
        ConnectionId=connection_id
    )

    return {
        "statusCode": 200,
        "body": 'Game created.'
    }

def trivia_joingame(event, _):
    "Lambda function to join a game"
    connection_id = event["requestContext"]["connectionId"]
    game_id = get_body_param(event, "gameid")

    # write the new connection into the dynamo table
    connection = {
        "gameId": game_id,
        "connectionId": connection_id,
        "playerName": get_random_player_name(),
        "score": 0
    }
    TABLE.put_item(Item=connection)

    players = get_players(game_id)
    send_broadcast(
        [p["connectionId"] for p in players],
        {"action": "playerlist", "players": players}
    )

    return {
        "statusCode": 200,
        "body": 'Joined game.'
    }


def trivia_startgame(event, _):
    "Lambda function to start a game"
    game_id = get_body_param(event, "gameid")
    state_machine = os.getenv("STATE_MACHINE")

    questions = QUESTIONS.copy()
    random.shuffle(questions)
    questions = questions[:10]

    machine_input = {
        "gameid": game_id,
        "questions": questions,
        "waitseconds": WAIT_SECONDS,
        "iterator": {
            "questionpos": 0,
            "IsGameOver": False
        }
    }

    STEPFUNCTIONS.start_execution(
        stateMachineArn=state_machine,
        name=f"game-{game_id}",
        input=json.dumps(machine_input)
    )

    players = get_players(game_id)
    send_broadcast([p["connectionId"] for p in players], {"action": "gamestarted"})

    return {
        "statusCode": 200,
        "body": 'Joined game.'
    }


def trivia_answer(event, _):
    "Lambda function for a player to post an answer"
    game_id = get_body_param(event, "gameid")
    questionid = get_body_param(event, "questionid")
    answer = get_body_param(event, "answer")
    connection_id = event["requestContext"]["connectionId"]

    TABLE.update_item(
        Key={"gameId": game_id, "connectionId": connection_id},
        AttributeUpdates={
            "lastQuestionId": {'Value': questionid, "Action": "PUT"},
            "lastAnswer": {'Value': answer, "Action": "PUT"}
        }
    )

    return {
        "statusCode": 200,
        "body": 'Recieved answer.'
    }

def trivia_question(event, _):
    "Send a question - called from statemachine"
    game_id = event["gameid"]
    question_pos = event["iterator"]["questionpos"]
    questions = event["questions"]
    question = event["questions"][question_pos]
    del question["answer"]
    question["question"] += f" {question_pos+1}/{len(questions)}"

    players = get_players(game_id)
    send_broadcast([
        p["connectionId"] for p in players],
        {"action": "question", "question": question}
    )

    return True

def trivia_calculate_scores(event, _):
    "Calc scores for a game - called from statemachine"
    game_id = event["gameid"]
    question_pos = event["iterator"]["questionpos"]
    questions = event["questions"]
    question = event["questions"][question_pos]

    connections = TABLE.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("gameId").eq(game_id)
    )

    # spin thru the connections and check their answers
    players = []
    for connection in connections["Items"]:
        connection_id = connection["connectionId"]
        player_name = connection["playerName"]
        score = int(connection["score"])
        last_question_id = connection["lastQuestionId"] if "lastQuestionId" in connection else ""
        last_answer = connection["lastAnswer"] if "lastAnswer" in connection else ""

        if last_question_id == question["id"] and last_answer == question["answer"]:
            score += 10
            TABLE.update_item(
                Key={"gameId": game_id, "connectionId": connection_id},
                AttributeUpdates={"score": {'Value': score, "Action": "PUT"}}
            )

        players.append({
            "connectionId" : connection_id,
            "playerName" : player_name,
            "score": score
        })

    # notify everyone the scores
    send_broadcast(
        [c["connectionId"] for c in connections["Items"]],
        {"action": "playerlist", "players": players}
    )

    question_pos += 1
    game_over = question_pos >= len(questions)
    if game_over:
        send_broadcast(
             [c["connectionId"] for c in connections["Items"]],
             {"action": "gameover"}
        )

    return {
                "questionpos": question_pos,
                "IsGameOver": game_over
            }
