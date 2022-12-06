using Amazon.S3;
using Amazon;
using Amazon.S3.Model;
using Amazon.S3.Util;

namespace CreateBucket;
public class CreateBucket
{
    public static async Task Main(string[] args)
    {
        IAmazonS3 s3Client = new AmazonS3Client(RegionEndpoint.USEast1);
        String bucketName = "<bucket name here>";

        BucketExists(s3Client, bucketName);
        await CreateBucketAsync(s3Client,bucketName);
        
    }
    private static void BucketExists(IAmazonS3 s3Client, string bucketName)
    {
        bool exists = AmazonS3Util.DoesS3BucketExistV2Async(s3Client, bucketName).Result;
        if(exists) {
            Console.WriteLine("This bucket already exists, exiting...");
            System.Environment.Exit(1);

        }
        else 
        {
            Console.WriteLine("The bucket does not exist, continuing...");
        }
    }

   public static async Task<bool> CreateBucketAsync(IAmazonS3 client, string bucketName)
    {
        try
        {
            var request = new PutBucketRequest
            {
                BucketName = bucketName,
                UseClientRegion = true,
            };

            var response = await client.PutBucketAsync(request);
            return response.HttpStatusCode == System.Net.HttpStatusCode.OK;
        }
        catch (AmazonS3Exception ex)
        {
            Console.WriteLine($"Error creating bucket: '{ex.Message}'");
            return false;
        }
    }
}

