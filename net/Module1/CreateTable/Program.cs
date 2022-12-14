using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;

namespace CreateTable;
public class Program
{
    public static async Task Main(string[] args)
    {
        // Create a client
        AmazonDynamoDBClient client = new AmazonDynamoDBClient();

        var tableName = "SampleTable11";

        var describeTableResponse = await client.DescribeTableAsync(new DescribeTableRequest
            { TableName = tableName });
        //Initial status of the table
        var status = describeTableResponse.Table.TableStatus;

        while (status != "ACTIVE")
        {// After the table is created, its status is set to ACTIVE 
            System.Threading.Thread.Sleep(5000); // Wait 5 seconds
                                                    //Get the latest table information.
            describeTableResponse = await client.DescribeTableAsync(new DescribeTableRequest
            { TableName = tableName });
            Console.WriteLine("Table name: {0}, status: {1}",
                    describeTableResponse.Table.TableName, describeTableResponse.Table.TableStatus);
            status = describeTableResponse.Table.TableStatus;
        }
    }
}
