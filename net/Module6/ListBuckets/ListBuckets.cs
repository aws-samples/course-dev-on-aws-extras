using Amazon.S3;
using Amazon.S3.Model;

namespace ListBuckets;
public class ListBuckets
{
    public static async Task Main()
    {
        IAmazonS3 s3Client = new AmazonS3Client();
        var response = await GetBuckets(s3Client);
        DisplayBucketList(response.Buckets);
    }
    public static async Task<ListBucketsResponse> GetBuckets(IAmazonS3 client)
    {
         return await client.ListBucketsAsync();
    }

    public static void DisplayBucketList(List<S3Bucket> bucketList)
    {
        bucketList
            .ForEach(b => Console.WriteLine($"Bucket name: {b.BucketName}, created on: {b.CreationDate}"));
    }  
}
