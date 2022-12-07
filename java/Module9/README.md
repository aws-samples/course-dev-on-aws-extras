The commands below are used to package and create a lambda function

``` bash
# create the jar file with a gradle build
# more details here: https://docs.aws.amazon.com/lambda/latest/dg/java-package.html
gradle build

# you can see the contents of the jar with the unzip utility
unzip -l build/libs/Module9.jar 

# grab the full ARN of the role created for the lambda function
ROLE_ARN=$(aws iam get-role --role-name lambda-basic-execution-role --query Role.Arn --output text)

# create the function
aws lambda create-function \
    --function-name hello-java \
    --runtime java11 \
    --zip-file fileb://build/libs/Module9.jar  \
    --handler software.amazon.samples.developingsamples.hello.App::handleRequest \
    --role $ROLE_ARN

# invoke the function
aws lambda invoke --function-name hello-java ~/output.txt
```

We can also update the configuration of the lambda function.

``` bash
# set the GREETING environment variable
aws lambda update-function-configuration \
    --function-name hello-java \
    --environment 'Variables={GREETING=Hola}'

# see the updated output
aws lambda invoke --function-name hello-java ~/output.txt
```
