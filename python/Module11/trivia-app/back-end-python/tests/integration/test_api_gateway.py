import os
from unittest import TestCase

import boto3
import requests
import asyncio
import websockets
import json

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test.
"""


class TestApiGateway(TestCase):
    api_endpoint: str

    @classmethod
    def get_stack_name(cls) -> str:
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")
        if not stack_name:
            raise Exception(
                "Cannot find env var AWS_SAM_STACK_NAME. \n"
                "Please setup this environment variable with the stack name where we are running integration tests."
            )

        return stack_name

    def setUp(self) -> None:
        """
        Based on the provided env variable AWS_SAM_STACK_NAME,
        here we use cloudformation API to find out what the TriviaWebSocketApi URL is
        """
        stack_name = TestApiGateway.get_stack_name()

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name}. \n" f'Please make sure stack with the name "{stack_name}" exists.'
            ) from e

        stacks = response["Stacks"]

        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "TriviaWebSocketApi"]
        self.assertTrue(api_outputs, f"Cannot find output TriviaWebSocketApi in stack {stack_name}")

        self.api_endpoint = api_outputs[0]["OutputValue"]

    def test_api_gateway(self):
        asyncio.get_event_loop().run_until_complete(self.simulate_game(self.api_endpoint))

    async def simulate_game(self, uri):
        async with websockets.connect(uri, compression=None) as websocket:
            # intitial new game
            print(f"sending websocket to {uri}")
            await websocket.send(json.dumps({"action":"newgame"}))
            game_created_message = json.loads(await websocket.recv())
            print(game_created_message)

            # start the game
            game_id = game_created_message['gameId']
            await websocket.send(json.dumps({"action":"startgame", "gameid": game_id}))

            # player list
            player_list_message = json.loads(await websocket.recv())
            print(player_list_message)
            # game started
            game_start_message= json.loads(await websocket.recv())
            print(game_start_message)

            # questions
            for i in range(10):
                # question
                question_message = json.loads(await websocket.recv())
                print(question_message)
                options = question_message['question']['options']
                question_id = question_message['question']['id']

                # send an answer
                await websocket.send(json.dumps({
                "action": "answer",
                "gameid": game_id,
                "questionid": question_id,
                "answer": options[0]
                }))

                # get the list / scores update
                player_list_message = json.loads(await websocket.recv())
                print(player_list_message)
