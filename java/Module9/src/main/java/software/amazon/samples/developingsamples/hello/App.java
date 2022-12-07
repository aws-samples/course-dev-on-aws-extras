package software.amazon.samples.developingsamples.hello;

import java.io.IOException;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

public class App implements RequestHandler<Object, String> {
    public String handleRequest(Object event, Context context) {
        String greeting = System.getenv("GREETING");
        if (greeting == null || greeting == "") {
            greeting = "Hello";
        }
        return greeting + " from Lambda!";
    }
}
