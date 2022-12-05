# python-sam-app

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

Build your application with the `sam build --use-container` command.

```bash
python-sam-app$ sam build --use-container
```

Run functions locally and invoke them with the `sam local invoke` command.

```bash
python-sam-app$ sam local invoke StarsFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
python-sam-app$ sam local start-api
python-sam-app$ curl http://localhost:3000/
```

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
python-sam-app$ sam logs -n StarsFunction --stack-name python-sam-app --tail
```

Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests.

```bash
python-sam-app$ pip install pytest pytest-mock --user
python-sam-app$ python -m pytest tests/ -v
```

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name python-sam-app
```
