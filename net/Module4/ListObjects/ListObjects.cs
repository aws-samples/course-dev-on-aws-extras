using Amazon.S3;
using Amazon.S3.Model;

namespace ListBuckets;
public class ListBuckets
{
        public static async Task Main()
        {

            string bucketName = Environment.GetEnvironmentVariable("MY_BUCKET");

            IAmazonS3 s3Client = new AmazonS3Client();

            Console.WriteLine($"Listing the objects contained in {bucketName}:\n");
            await ListingObjectsAsync(s3Client, bucketName);
        }

    public static async Task ListingObjectsAsync(IAmazonS3 client, string bucketName)
    {
        var listObjectsV2Paginator = client.Paginators.ListObjectsV2(new ListObjectsV2Request
        {
            BucketName = bucketName,
        });

        await foreach (var response in listObjectsV2Paginator.Responses)
        {
            Console.WriteLine($"HttpStatusCode: {response.HttpStatusCode}");
            Console.WriteLine($"Number of Keys: {response.KeyCount}");
            foreach (var entry in response.S3Objects)
            {
                Console.WriteLine($"Key = {entry.Key} Size = {entry.Size}");
            }
        }
    }
}
