using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;

namespace DynamoDBTables
{
    public class DynamoDBTables
    {
        private static readonly string _tableName = "Notes";

        public static async Task<bool> CreateExampleTable(AmazonDynamoDBClient client)
        {
            Console.WriteLine("\n*** Creating table ***");
            var request = new CreateTableRequest
            {
                AttributeDefinitions = new List<AttributeDefinition>()
            {
                new AttributeDefinition
                {
                    AttributeName = "Id",
                    AttributeType = "N"
                }
            },
                KeySchema = new List<KeySchemaElement>
            {
                new KeySchemaElement
                {
                    AttributeName = "Id",
                    KeyType = "HASH" //Partition key
                }
            },
                ProvisionedThroughput = new ProvisionedThroughput
                {
                    ReadCapacityUnits = 10,
                    WriteCapacityUnits = 10
                },
                TableName = _tableName
            };

            try 
            {
                var response = await client.CreateTableAsync(request);
                var tableDescription = response.TableDescription;
                Console.WriteLine("{1}: {0} \t ReadsPerSec: {2} \t WritesPerSec: {3}",
                        tableDescription.TableStatus,
                        tableDescription.TableName,
                        tableDescription.ProvisionedThroughput.ReadCapacityUnits,
                        tableDescription.ProvisionedThroughput.WriteCapacityUnits);

                string status = tableDescription.TableStatus;
                Console.WriteLine(_tableName + " - " + status);

                await WaitUntilTableReady(client);
                return true;
            } catch(Exception e) {
                Console.WriteLine(e.Message);
            }  

            return false;
        }

        public static async Task<bool> ListMyTables(AmazonDynamoDBClient client)
        {
            Console.WriteLine("\n*** listing tables ***");
           
            var request = new ListTablesRequest();

            var response = await client.ListTablesAsync(request);
            foreach (string name in response.TableNames)
                Console.WriteLine(name);

            return true;
        }


        public static async Task<bool> UpdateExampleTable(AmazonDynamoDBClient client)
        {
            Console.WriteLine("\n*** Updating table ***");
            var request = new UpdateTableRequest()
            {
                TableName = _tableName,
                ProvisionedThroughput = new ProvisionedThroughput()
                {
                    ReadCapacityUnits = 6,
                    WriteCapacityUnits = 6
                }
            };

            await client.UpdateTableAsync(request);

            await WaitUntilTableReady(client);

            return true;
        }

        public static async Task<bool> DeleteExampleTable(AmazonDynamoDBClient client)
        {
            Console.WriteLine("\n*** Deleting table ***");
            var request = new DeleteTableRequest
            {
                TableName = _tableName
            };

            await client.DeleteTableAsync(request);

            Console.WriteLine("Table is being deleted...");

            return true;
        }

        private static async Task<bool> WaitUntilTableReady(AmazonDynamoDBClient client)
        {
            string status;
            // Let us wait until table is created or updated. Call DescribeTable.
            do
            {
                System.Threading.Thread.Sleep(5000); // Wait 5 seconds.
                var res = await client.DescribeTableAsync(new DescribeTableRequest
                {
                    TableName = _tableName
                });

                Console.WriteLine("Table name: {0}, status: {1}",
                          res.Table.TableName,
                          res.Table.TableStatus);
                status = res.Table.TableStatus;

            } while (status != "ACTIVE");

            return true;
        }

        static void Main()
        {
            var client = new AmazonDynamoDBClient();

            var result = CreateExampleTable(client);

            if (!result.Result)
            {
                Console.WriteLine("Could not create example table.");
            }

            result = ListMyTables(client);

            if (!result.Result)
            {
                Console.WriteLine("Could not list tables.");
                Console.WriteLine("You must delete the " + _tableName + " table yourself");
            }


            result = UpdateExampleTable(client);

            if (!result.Result)
            {
                Console.WriteLine("Could not update example table.");
                Console.WriteLine("You must delete the " + _tableName + " table yourself");
            }

            result = DeleteExampleTable(client);

            if (!result.Result)
            {
                Console.WriteLine("Could not delete example table.");
                Console.WriteLine("You must delete the " + _tableName + " table yourself");
            }
        }
    }
}