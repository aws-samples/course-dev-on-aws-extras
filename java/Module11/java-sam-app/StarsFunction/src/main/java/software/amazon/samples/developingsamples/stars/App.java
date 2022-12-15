package software.amazon.samples.developingsamples.stars;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import com.jcabi.github.Coordinates;
import com.jcabi.github.Github;
import com.jcabi.github.Repo;
import com.jcabi.github.RtGithub;

/**
 * Handler for requests to Lambda function.
 */
public class App implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {

    public APIGatewayProxyResponseEvent handleRequest(final APIGatewayProxyRequestEvent input, final Context context) {
        Map<String, String> headers = new HashMap<>();
        headers.put("Content-Type", "application/json");
        headers.put("access-control-allow-origin", "*");


        APIGatewayProxyResponseEvent response = new APIGatewayProxyResponseEvent()
                .withHeaders(headers);
 
        Github github = new RtGithub();
        String user = "aws";
        String respository = "aws-sdk-java";
        Repo repo = github.repos().get(new Coordinates.Simple(user, respository));
        try {
            String output = String.format("{ \"repository\":  \"%s/%s\",  \"stargazers_count\":  \"%d\" }",
                user,
                respository,
                repo.json().getInt("stargazers_count"));
            return response
            .withStatusCode(200)
            .withBody(output);

        } catch (IOException e) {
            return response
                    .withBody("{}")
                    .withStatusCode(500);
        }

    }

}
