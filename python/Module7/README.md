The commands below are used to package and create a lambda function

``` bash
# zip the function - we can also include dependencies in the root of the zip
# more details here: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
zip ~/hello-python.zip lambda_function.py 

# grab the full ARN of the role created for the lambda function
ROLE_ARN=$(aws iam get-role --role-name lambda-basic-execution-role --query Role.Arn --output text)

# create the function
aws lambda create-function \
    --function-name hello-python \
    --runtime python3.9 \
    --zip-file fileb://~/hello-python.zip \
    --handler lambda_function.lambda_handler \
    --role $ROLE_ARN

# invoke the function
aws lambda invoke --function-name hello-python ~/output.txt
```

We can also update the configuration of the lambda function.

``` bash
# set the GREETING environment variable
aws lambda update-function-configuration \
    --function-name hello-python \
    --environment 'Variables={GREETING=Hola}'

# see the updated output
aws lambda invoke --function-name hello-python ~/output.txt
```
