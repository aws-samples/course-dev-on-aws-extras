using Amazon.S3;
using Amazon.S3.Model;
using Amazon;
using System.Text;

namespace S3Select;
public class S3Select
{
    public static async Task Main(string[] args)
    {
        string bucketName = Environment.GetEnvironmentVariable("MY_BUCKET");
        string objectKey = "airports.csv";

        IAmazonS3 s3Client = new AmazonS3Client(RegionEndpoint.USEast1);
        await QueryS3(s3Client, bucketName, objectKey);
    }

    private async static Task QueryS3(IAmazonS3 s3Client, string bucketName, string objectKey) {

        var selectRequest = new SelectObjectContentRequest
        {
            BucketName = bucketName,
            Key = objectKey,
            Expression = "select * from s3object s where s.\"iso_country\" like '%US%'",
            ExpressionType = ExpressionType.SQL,
            InputSerialization = new InputSerialization
            {
                CSV = new CSVInput
                {
                    FileHeaderInfo = FileHeaderInfo.Use
                }
            },
            OutputSerialization = new OutputSerialization
            {
                CSV = new CSVOutput()
            }
        };

        var response = await s3Client.SelectObjectContentAsync(selectRequest);

        var payload = response.Payload;

        using (payload)
            {
                foreach (var ev in payload)
                {
                    if (ev is RecordsEvent records)
                    {
                        using (var reader = new StreamReader(records.Payload, Encoding.UTF8))
                        {
                            while (reader.Peek() >= 0)
                            {
                               Console.WriteLine(reader.ReadLine());
                            }
                        }
                    }
                }
            }
    }
}
