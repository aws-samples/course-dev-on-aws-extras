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
        await PrintObjectMetadata(s3Client, bucketName, keyName);
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

    public static async Task PrintObjectMetadata(IAmazonS3 client, string bucketName, string objectName) {
        // Read more about the GetObjectAttributesAsync call here:
        // https://docs.aws.amazon.com/sdkfornet/v3/apidocs/items/S3/MS3GetObjectAttributesAsyncGetObjectAttributesRequestCancellationToken.html 
        List<ObjectAttributes> objectAttributes = new List<ObjectAttributes>();
        objectAttributes.Add("StorageClass");
        objectAttributes.Add("ObjectSize");

        GetObjectAttributesRequest request = new GetObjectAttributesRequest{
            BucketName = bucketName,
            Key = objectName,
            ObjectAttributes = objectAttributes
        };

        CancellationToken token = new CancellationToken();

        GetObjectAttributesResponse response = await client.GetObjectAttributesAsync(request, token);

        Console.WriteLine("Object storage class: " + response.StorageClass + " , Object size: " + response.ObjectSize);

        
    }
}
