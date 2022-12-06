using Amazon.S3;
using Amazon;
using Amazon.S3.Model;

namespace GetObject;
public class GetObject
{
    public static async Task Main(string[] args)
    {
        string bucketName = Environment.GetEnvironmentVariable("MY_BUCKET");
        string keyName = "airports.csv";

        IAmazonS3 s3Client = new AmazonS3Client(RegionEndpoint.USEast1);
        await ReadObjectDataAsync(s3Client, bucketName, keyName);
    }

  public static async Task<bool> ReadObjectDataAsync(IAmazonS3 client, string bucketName, string objectName)
    {
        var request = new GetObjectRequest
        {
            BucketName = bucketName,
            Key = objectName,
        };

        using GetObjectResponse response = await client.GetObjectAsync(request);

        try
        {
            await response.WriteResponseStreamToFileAsync($"C://Temp/\\{objectName}", true, CancellationToken.None);
            return response.HttpStatusCode == System.Net.HttpStatusCode.OK;
        }
        catch (AmazonS3Exception ex)
        {
            Console.WriteLine($"Error saving {objectName}: {ex.Message}");
            return false;
        }
    }
}
