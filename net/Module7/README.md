The commands below are used to package and create a lambda function. More details on C# code packaging at: https://docs.aws.amazon.com/lambda/latest/dg/csharp-package-cli.html

``` bash
# install the .NET Core Global Tool
dotnet tool install -g Amazon.Lambda.Tools

# grab the full ARN of the role created for the lambda function
ROLE_ARN=$(aws iam get-role --role-name lambda-basic-execution-role --query Role.Arn --output text)

# deploy the function
dotnet lambda deploy-function hello-dotnet --function-role $ROLE_ARN

# we can see the contents of the zip that was deployed
unzip -l bin/Release/net6.0/Module9.zip

# invoke the function
aws lambda invoke --function-name hello-dotnet ~/output.txt
```

We can also update the configuration of the lambda function.

``` bash
# set the GREETING environment variable
aws lambda update-function-configuration \
    --function-name hello-dotnet \
    --environment 'Variables={GREETING=Hola}'

# see the updated output
aws lambda invoke --function-name hello-dotnet ~/output.txt
```
