package software.amazon.samples.developingsamples.module8;

import software.amazon.awssdk.core.waiters.WaiterResponse;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;
import software.amazon.awssdk.services.dynamodb.waiters.DynamoDbWaiter;

import java.util.List;

public class CreateTable
{
    public static void main(String[] args) {
        DynamoDbClient ddb = DynamoDbClient.builder().build();
        String tableName = "Notes";
        String keyName = "NotesID";

        System.out.println("Listing tables...");
        listTables(ddb);

        System.out.println("Creating notes table...");
        boolean result = createTable(ddb, tableName, keyName);

        if(result) {
            System.out.println("New table is " + result);
            System.out.println("Updating table throughput...");
            updateTable(ddb, tableName);
            System.out.println("Deleting table...");
            deleteTable(ddb, tableName);
            System.out.println("Table has been deleted");
        }
        ddb.close();
    }

    public static boolean createTable(DynamoDbClient ddb, String tableName, String key) {
        DynamoDbWaiter dbWaiter = ddb.waiter();
        CreateTableRequest request = CreateTableRequest.builder()
                .attributeDefinitions(AttributeDefinition.builder()
                        .attributeName(key)
                        .attributeType(ScalarAttributeType.S)
                        .build())
                .keySchema(KeySchemaElement.builder()
                        .attributeName(key)
                        .keyType(KeyType.HASH)
                        .build())
                .provisionedThroughput(ProvisionedThroughput.builder()
                        .readCapacityUnits(new Long(10))
                        .writeCapacityUnits(new Long(10))
                        .build())
                .tableName(tableName)
                .build();

        boolean tableCreated = false;
        try {
            CreateTableResponse response = ddb.createTable(request);
            DescribeTableRequest tableRequest = DescribeTableRequest.builder()
                    .tableName(tableName)
                    .build();

            // Wait until the Amazon DynamoDB table is created.
            WaiterResponse<DescribeTableResponse> waiterResponse = dbWaiter.waitUntilTableExists(tableRequest);
            waiterResponse.matched().response().ifPresent(System.out::println);
            tableCreated = true;

        } catch (DynamoDbException e) {
            System.err.println(e.getMessage());
        }
        return tableCreated;
    }

    public static void updateTable(DynamoDbClient ddb, String tableName) {
        ProvisionedThroughput tableThroughput = ProvisionedThroughput.builder()
                .readCapacityUnits(5L)
                .writeCapacityUnits(5L)
                .build();

        UpdateTableRequest request = UpdateTableRequest.builder()
                .tableName(tableName)
                .provisionedThroughput(tableThroughput)
                .build();

        try{
            ddb.updateTable(request);
        } catch (DynamoDbException e) {
            System.out.println(e.getMessage());
        }
    }

    public static void deleteTable(DynamoDbClient ddb, String tableName) {
        DeleteTableRequest request = DeleteTableRequest.builder()
                .tableName(tableName)
                .build();

        try {
            ddb.deleteTable(request);

        } catch (DynamoDbException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }
        System.out.println(tableName +" was successfully deleted!");
    }

    public static void listTables(DynamoDbClient ddb) {
        try {

            ListTablesRequest request = ListTablesRequest.builder().build();
            ListTablesResponse response = ddb.listTables(request);

            List<String> tableNames = response.tableNames();
            if (tableNames.size() > 0) {
                for (String curName : tableNames) {
                    System.out.format("* %s\n", curName);
                }
            } else {
                System.out.println("No tables found!");
                System.exit(0);
            }
        } catch (DynamoDbException e) {
            System.err.println(e.getMessage());
            System.exit(1);
        }
    }
}
