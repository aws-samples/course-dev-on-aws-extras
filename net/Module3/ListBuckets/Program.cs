using Amazon.S3;
using Amazon.S3.Model;

namespace CreateBucket;
class Program
{
    static async Task Main(string[] args)
    {
        AmazonS3Config S3Config = new AmazonS3Config();

        // Create S3 client object
        AmazonS3Client s3Client = new AmazonS3Client(S3Config);

        // Total number of buckets owned by the user and a list of them
        var listResponse = await s3Client.ListBucketsAsync();
        Console.WriteLine($"Total buckets: {listResponse.Buckets.Count}");
        foreach (S3Bucket b in listResponse.Buckets)
        {
            Console.WriteLine(b.BucketName);
        }
    }
}
