using Amazon.S3.Util;
using Amazon.S3;
using Amazon;

namespace VerifyBucketName;
public class VerifyBucketName
{
    public static void Main(string[] args)
    {
        string bucketName = Environment.GetEnvironmentVariable("MY_BUCKET");
        IAmazonS3 s3Client = new AmazonS3Client(RegionEndpoint.USEast1);
        VerifyBucket(s3Client, bucketName);
    }

    private static async void VerifyBucket(IAmazonS3 s3Client, string bucketName)
    {
        bool exists = false;

        exists = AmazonS3Util.DoesS3BucketExistV2Async(s3Client, bucketName).Result;
        if(exists) {
            Console.WriteLine("This bucket already exists.");
        }
        else 
        {
            Console.WriteLine("The bucket does not exist.");
        }
    }
}
