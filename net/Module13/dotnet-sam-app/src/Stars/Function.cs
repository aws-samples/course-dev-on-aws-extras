using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text.Json;

using Amazon.Lambda.Core;
using Amazon.Lambda.APIGatewayEvents;
using Octokit;

// Assembly attribute to enable the Lambda function's JSON input to be converted into a .NET class.
[assembly: LambdaSerializer(typeof(Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer))]

namespace Stars
{

    public class Function
    {

        public async Task<APIGatewayProxyResponse> FunctionHandler(APIGatewayProxyRequest apigProxyEvent, ILambdaContext context)
        {
            var github = new GitHubClient(new ProductHeaderValue("SampleApp"));
            string user = "aws";
            string repo = "aws-sdk-net";

            var repository = await github.Repository.Get(user, repo);

            var body = new Dictionary<string, string>
            {
                { "repository", $"{user}/{repo}"},
                { "stargazers_count", repository.StargazersCount.ToString() }
            };

            return new APIGatewayProxyResponse
            {
                Body = JsonSerializer.Serialize(body),
                StatusCode = 200,
                Headers = new Dictionary<string, string> { { "Content-Type", "application/json" }, { "access-control-allow-origin", "*" } }
            };
        }
    }
}
