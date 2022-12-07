from gameactions import app
from botocore.exceptions import ClientError

import uuid
import json
from unittest import mock

NEW_GAME_EVENT = {
        "requestContext": {
            "connectionId" : "connection-123"
        }
    }

JOIN_GAME_EVENT = {
        "requestContext": {
            "connectionId" : "connection-joining-123"
        },
        "body" : json.dumps({"gameid" : "01234567012301230123012345678901"})
    }

START_GAME_EVENT = {
    "body" : json.dumps({"gameid" : "01234567012301230123012345678901"})
}

ANSWER_EVENT = {
        "requestContext": {
            "connectionId" : "connection-answer-123"
        },
        "body" : json.dumps({
            "gameid" : "01234567012301230123012345678901",
            "questionid" : "q-1234",
            "answer" : "Answer"
            })
    }

QUESTION_EVENT = {
        "gameid" : "01234567012301230123012345678901",
        "questions" : [{ "id" : "q-1234", "question" : "Question?", "answer" : "Answer"}],
        "iterator" : { "questionpos" : 0 }
}

SCORES_EVENT = {
        "gameid" : "01234567012301230123012345678901",
        "questions" : [
            { "id" : "q-1111", "question" : "Good question?", "answer" : "Yes"},
        ],
        "iterator" : { "questionpos" : 0 }
}

SCORES_EVENT_TWO = {
        "gameid" : "01234567012301230123012345678901",
        "questions" : [
            { "id" : "q-1111", "question" : "Good question?", "answer" : "Yes"},
            { "id" : "q-1112", "question" : "Second question?", "answer" : "Yes"},
        ],
        "iterator" : { "questionpos" : 0 }
}


def test_trivia_newgame(mocker):
    # create mocks
    mocker.patch.object(app, 'TABLE')
    mocker.patch.object(app, 'MANAGEMENT')
    mocker.patch('uuid.uuid4', return_value=uuid.UUID('01234567-0123-0123-0123-012345678901'))
    mocker.patch('random.choice', side_effect=lambda seq: seq[0])


    # call the lambda entry point
    app.trivia_newgame(NEW_GAME_EVENT, None)

    # assert we call dynamo with a row for the game
    app.TABLE.put_item.assert_called_with(
        Item={
            "gameId":"01234567012301230123012345678901",
            "connectionId": "connection-123",
            'playerName': 'AliceBlue',
            "score": 0
            })

    # assert the post_to_connection calls to the connection that created the game
    app.MANAGEMENT.post_to_connection.assert_has_calls([
        mock.call(Data='{"action": "gamecreated", "gameId": "01234567012301230123012345678901"}', ConnectionId='connection-123'),
        mock.call(Data='{"action": "playerlist", "players": [{"connectionId": "connection-123", "currentPlayer": true, "playerName": "AliceBlue", "score": 0}]}',
          ConnectionId='connection-123')
        ])

def test_trivia_joingame(mocker):
    # create mocks
    mocker.patch.object(app, 'TABLE')
    mocker.patch.object(app, 'MANAGEMENT')
    mocker.patch('random.choice', side_effect=lambda seq: seq[0])

    # mock the response from the game table
    app.TABLE.query.return_value = {'Items':[{'connectionId': "connection-1", "playerName" : "AliceBlue", "score" : "10"}]}

    # call the lambda entry point
    app.trivia_joingame(JOIN_GAME_EVENT, None)

    # assert we insert the joined player
    app.TABLE.put_item.assert_called_with(
        Item={
            'gameId': '01234567012301230123012345678901',
            'connectionId': 'connection-joining-123',
            'playerName': 'AliceBlue',
            'score': 0
            })
    # assert the post_to_connection sends a new player list
    app.MANAGEMENT.post_to_connection.assert_called_with(
        Data='{"action": "playerlist", "players": [{"connectionId": "connection-1", "playerName": "AliceBlue", "score": 10, "currentPlayer": true}]}', ConnectionId='connection-1'
    )

def test_trivia_startgame(mocker):
    # create mocks
    mocker.patch.object(app, 'TABLE')
    mocker.patch.object(app, 'MANAGEMENT')
    mocker.patch.object(app, 'STEPFUNCTIONS')

    # mock the response from the game table
    app.TABLE.query.return_value = {'Items':[{'connectionId': "connection-1", "playerName" : "AliceBlue", "score" : "10"}]}

    # call the lambda entry point
    app.trivia_startgame(START_GAME_EVENT, None)

    # assert call to stepfunctions
    assert app.STEPFUNCTIONS.start_execution.call_count == 1

    # assert the gamestarted is sent
    app.MANAGEMENT.post_to_connection.assert_called_with(
        Data='{"action": "gamestarted"}', ConnectionId='connection-1'
    )

def test_trivia_answer(mocker):
    # create mocks
    mocker.patch.object(app, 'TABLE')

    # call the lambda entry point
    app.trivia_answer(ANSWER_EVENT, None)

    # assert we updated the game item
    app.TABLE.update_item.assert_called_with(
        Key={'gameId': '01234567012301230123012345678901', 'connectionId': 'connection-answer-123'},
        AttributeUpdates={'lastQuestionId': {'Value': 'q-1234', 'Action': 'PUT'}, 'lastAnswer': {'Value': 'Answer', 'Action': 'PUT'}}
    )

def test_trivia_question(mocker):
    # create mocks
    mocker.patch.object(app, 'TABLE')
    mocker.patch.object(app, 'MANAGEMENT')

    # mock the response from the game table
    app.TABLE.query.return_value = {'Items':[{'connectionId': "connection-1", "playerName" : "AliceBlue", "score" : "10"}]}

    # call the lambda entry point
    app.trivia_question(QUESTION_EVENT, None)

    app.MANAGEMENT.post_to_connection.assert_called_with(
        Data='{"action": "question", "question": {"id": "q-1234", "question": "Question? 1/1"}}',
        ConnectionId='connection-1'
    )



def test_trivia_calculate_scores_correct(mocker):
    mocker.patch.object(app, 'TABLE')
    mocker.patch.object(app, 'MANAGEMENT')

    # mock a correct response from the game table
    app.TABLE.query.return_value = {'Items':[
        {
            "connectionId": "connection-1",
            "gameId": "01234567012301230123012345678901",
            "playerName" : "AliceBlue",
            "lastAnswer": "Yes",
            "lastQuestionId": "q-1111",
            "score": 0
        }
    ]}

    app.trivia_calculate_scores(SCORES_EVENT, None)

    # assert we updated the game item, score is incremented
    app.TABLE.update_item.assert_called_with(
        Key={'gameId': '01234567012301230123012345678901', 'connectionId': 'connection-1'},
        AttributeUpdates={'score': {'Value': 10, 'Action': 'PUT'}}
    )

    app.MANAGEMENT.post_to_connection.assert_has_calls([
        mock.call(Data='{"action": "playerlist", "players": [{"connectionId": "connection-1", "playerName": "AliceBlue", "score": 10, "currentPlayer": true}]}', ConnectionId='connection-1'),
        mock.call(Data='{"action": "gameover"}', ConnectionId='connection-1')
        ])


def test_trivia_calculate_scores_wrong(mocker):
    mocker.patch.object(app, 'TABLE')
    mocker.patch.object(app, 'MANAGEMENT')

    # mock a correct response from the game table
    app.TABLE.query.return_value = {'Items':[
        {
            "connectionId": "connection-1",
            "gameId": "01234567012301230123012345678901",
            "playerName" : "AliceBlue",
            "lastAnswer": "No",
            "lastQuestionId": "q-1111",
            "score": 0
        }
    ]}

    app.trivia_calculate_scores(SCORES_EVENT_TWO, None)

    # score not incremented
    app.MANAGEMENT.post_to_connection.assert_called_with(
        Data='{"action": "playerlist", "players": [{"connectionId": "connection-1", "playerName": "AliceBlue", "score": 0, "currentPlayer": true}]}',
        ConnectionId='connection-1'
    )


def test_broadcast_connection_gone(mocker):
    # create mocks
    mocker.patch.object(app, 'TABLE')
    mocker.patch.object(app, 'MANAGEMENT')

    # mock the response from the game table
    app.TABLE.query.return_value = {'Items':[{'connectionId': "connection-1", "playerName" : "AliceBlue", "score" : "10"}]}

    app.MANAGEMENT.post_to_connection.side_effect = ClientError(
        {
            'Error': {'Code': 'GoneException'}
        },
        'PostToConnection'
    )

    app.send_broadcast("01234567012301230123012345678901", {})


def test_broadcast_other_error(mocker):
    # create mocks
    mocker.patch.object(app, 'TABLE')
    mocker.patch.object(app, 'MANAGEMENT')

    # mock the response from the game table
    app.TABLE.query.return_value = {'Items':[{'connectionId': "connection-1", "playerName" : "AliceBlue", "score" : "10"}]}

    app.MANAGEMENT.post_to_connection.side_effect = ClientError(
        {
            'Error': {'Code': 'Anything'}
        },
        'PostToConnection'
    )
    app.send_broadcast("01234567012301230123012345678901", {})
