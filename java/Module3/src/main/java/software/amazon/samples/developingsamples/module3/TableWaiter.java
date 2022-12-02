package software.amazon.samples.developingsamples.module3;

import software.amazon.awssdk.core.waiters.WaiterResponse;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.DescribeTableResponse;
import software.amazon.awssdk.services.dynamodb.waiters.DynamoDbWaiter;

public class TableWaiter {

    public static void main(String[] args) {
        DynamoDbClient dynamo = DynamoDbClient.create();
        DynamoDbWaiter waiter = dynamo.waiter();

        WaiterResponse<DescribeTableResponse> waiterResponse = waiter
                .waitUntilTableExists(r -> r.tableName("Employees"));

        // print out the matched response with a tableStatus of ACTIVE
        waiterResponse.matched().response().ifPresent(System.out::println);
    }

}
