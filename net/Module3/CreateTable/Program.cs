using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;

namespace CreateTable;
public class Program
{
    public static async Task Main(string[] args)
    {
        // Create a client
        AmazonDynamoDBClient client = new AmazonDynamoDBClient();

        // Define table schema:
        //  Table has a hash-key "Author" and a range-key "Title"
        List<KeySchemaElement> schema = new List<KeySchemaElement>
        {
            new KeySchemaElement
            {
                AttributeName = "Author", KeyType = "HASH"
            },
            new KeySchemaElement
            {
                AttributeName = "Title", KeyType = "RANGE"
            }
        };

        // Define key attributes:
        //  The key attributes "Author" and "Title" are string types
        List<AttributeDefinition> definitions = new List<AttributeDefinition>
        {
            new AttributeDefinition
            {
                AttributeName = "Author", AttributeType = "S"
            },
            new AttributeDefinition
            {
                AttributeName = "Title", AttributeType = "S"
            }
        };

        // Define table throughput:
        //  Table has capacity of 20 reads and 50 writes
        ProvisionedThroughput throughput = new ProvisionedThroughput
        {
            ReadCapacityUnits = 20,
            WriteCapacityUnits = 50
        };

        var tableName = "SampleTable11";
        // Configure the CreateTable request
        CreateTableRequest request = new CreateTableRequest
        {
            TableName = tableName,
            KeySchema = schema,
            ProvisionedThroughput = throughput,
            AttributeDefinitions = definitions
        };
        // creates a table with "request" information such as table name
        var response = await client.CreateTableAsync(request);
        var tableDescription = response.TableDescription;

        //Initial status of the table
        var status = tableDescription.TableStatus;

        while (status != "ACTIVE")
        {// After the table is created, its status is set to ACTIVE 
            System.Threading.Thread.Sleep(5000); // Wait 5 seconds
                                                    //Get the latest table information.
            var describeTableResponse = await client.DescribeTableAsync(new DescribeTableRequest
            { TableName = tableName });
            Console.WriteLine("Table name: {0}, status: {1}",
                    describeTableResponse.Table.TableName, describeTableResponse.Table.TableStatus);
            status = describeTableResponse.Table.TableStatus;
        }
    }
}
