
The application expects some Cognito settings in parameter store:

``` bash
aws ssm put-parameter --name PYDEMO_COGNITO_DOMAIN --value "<REPLACE_ME>" --type String
aws ssm put-parameter --name PYDEMO_COGNITO_CLIENT_ID --value "<REPLACE_ME>" --type String
aws ssm put-parameter --name PYDEMO_COGNITO_CLIENT_SECRET --value "<REPLACE_ME>" --type String
```