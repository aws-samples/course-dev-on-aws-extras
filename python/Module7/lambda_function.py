import os

def lambda_handler(event, context):
    greeting = os.getenv("GREETING", "hello")
    return f"{greeting} from my lambda function"