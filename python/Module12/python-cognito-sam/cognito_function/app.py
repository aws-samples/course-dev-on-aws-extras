import json
import requests
from requests.auth import HTTPBasicAuth
from jose import jwt
import boto3

# retrieve cognito settings from parameter store
ssm_parameters = boto3.client('ssm').get_parameters(
    Names=['PYDEMO_COGNITO_DOMAIN', "PYDEMO_COGNITO_CLIENT_ID", "PYDEMO_COGNITO_CLIENT_SECRET"]
)
COGNITO_DOMAIN = next(p["Value"] for p in ssm_parameters["Parameters"] if p["Name"] =='PYDEMO_COGNITO_DOMAIN')
COGNITO_CLIENT_ID = next(p["Value"] for p in ssm_parameters["Parameters"] if p["Name"] =='PYDEMO_COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = next(p["Value"] for p in ssm_parameters["Parameters"] if p["Name"] =='PYDEMO_COGNITO_CLIENT_SECRET')

with open('templates/index.html', 'r') as content_file:
    index_template = content_file.read()

def home_handler(event, context):
    # http://docs.aws.amazon.com/cognito/latest/developerguide/login-endpoint.html
    # we could improve security with "csrf_state"
    host = event["headers"]["Host"]
    path = event["requestContext"]["path"]
    proto = event["headers"]["X-Forwarded-Proto"]
    redirect_uri = f"{proto}://{host}{path}token"

    # build the cognito hosted login URL
    cognito_login = ("https://%s/"
                     "login?response_type=code&client_id=%s"
                     "&redirect_uri=%s" %
                     (COGNITO_DOMAIN, COGNITO_CLIENT_ID, redirect_uri))
    html = index_template.replace("%%PLACEHOLDER_BODY%%", f'Click the Login URL -> <a href="{cognito_login}">{cognito_login}</a>')

    return {
        "statusCode": 200,
        "headers": { "Content-Type": "text/html; charset=UTF-8" },
        "body": html,
    }

def token_handler(event, context):
    # check if we have a "code" parameter in the querystring
    if not event["queryStringParameters"] or "code" not in event["queryStringParameters"]:
        html = index_template.replace("%%PLACEHOLDER_BODY%%", 'This page expects a code parameter')
        return {
            "statusCode": 200,
            "headers": { "Content-Type": "text/html; charset=UTF-8" },
            "body": html,
        }

    host = event["headers"]["Host"]
    path = event["requestContext"]["path"]
    proto = event["headers"]["X-Forwarded-Proto"]
    redirect_uri = f"{proto}://{host}{path}"
    code = event["queryStringParameters"]['code']

    # we want to exchange the "code" from cognito for a token, this process is documented here:
    # http://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
    request_parameters = {'grant_type': 'authorization_code',
                          'client_id': COGNITO_CLIENT_ID,
                          'code': code,
                          "redirect_uri" : redirect_uri}
    response = requests.post("https://%s/oauth2/token" % COGNITO_DOMAIN,
                             data=request_parameters,
                             auth=HTTPBasicAuth(COGNITO_CLIENT_ID,
                                                COGNITO_CLIENT_SECRET))

    # cognito gives us an unhappy response
    if response.status_code != requests.codes.ok:
        html = index_template.replace("%%PLACEHOLDER_BODY%%", 'Unable to verify Cognito code')
        return {
            "statusCode": 200,
            "headers": { "Content-Type": "text/html; charset=UTF-8" },
            "body": html,
        }

    # decode the id and access token we received from cognito
    id_token = response.json()["id_token"]
    access_token = response.json()["access_token"]
    # this code should be retrieving JSON Web Key (JWK)
    # https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-    oviders.html
    info = jwt.decode(id_token, key=None, options={"verify_signature": False}, audience=COGNITO_CLIENT_ID, access_token=access_token)

    table = f"""<table class="table">
        <tr><td>cognito:username</td><td>{info["cognito:username"]}</td></tr>
        <tr><td>email</td><td>{info["email"]}</td></tr>"""
    if "nickname" in info:
        table = table + f"""<tr><td>nickname</td><td>{info["nickname"]}</td></tr>"""
    table = table + """</table>"""

    html = index_template.replace("%%PLACEHOLDER_BODY%%", table)
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "text/html; charset=UTF-8" },
        "body": html,
    }