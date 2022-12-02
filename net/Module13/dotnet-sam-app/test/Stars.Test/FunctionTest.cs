using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Net.Http;
using System.Text.Json;
using Xunit;
using Amazon.Lambda.TestUtilities;
using Amazon.Lambda.APIGatewayEvents;

namespace Stars.Tests
{
  public class FunctionTest
  {
    [Fact]
    public async Task TestStarsFunctionHandler()
    {
            var request = new APIGatewayProxyRequest();
            var context = new TestLambdaContext();

            var expectedResponse = new APIGatewayProxyResponse
            {
                StatusCode = 200,
                Headers = new Dictionary<string, string> { { "Content-Type", "application/json" }, { "access-control-allow-origin", "*" } }
            };

            var function = new Function();
            var response = await function.FunctionHandler(request, context);

            Console.WriteLine("Lambda Response: \n" + response.Body);
            Console.WriteLine("Expected Response: \n" + expectedResponse.Body);

            Assert.Contains("stargazers_count", response.Body);
            Assert.Contains("repository", response.Body);
            Assert.Equal(expectedResponse.Headers, response.Headers);
            Assert.Equal(expectedResponse.StatusCode, response.StatusCode);
    }
  }
}