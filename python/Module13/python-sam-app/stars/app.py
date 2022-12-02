import json
from octokit import Octokit

def lambda_handler(event, context):
    # load some info about the boto3 repo
    owner = "boto"
    repository="boto3"
    repos = Octokit().repos.get(owner=owner, repo=repository)
  
    return {
        "statusCode": 200,
        "headers": { "access-control-allow-origin": "*" },
        "body": json.dumps({
            "repository": F"{owner}/{repository}",
            "stargazers_count": repos.response.stargazers_count,
        }),
    }
