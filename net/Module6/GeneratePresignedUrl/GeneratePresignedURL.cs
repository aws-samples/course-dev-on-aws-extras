using Amazon.S3;
using Amazon;
using Amazon.S3.Model;

namespace GeneratePresignedUrl;
public class GetObject
{
    public static void Main(string[] args)
    {
        string bucketName = Environment.GetEnvironmentVariable("MY_BUCKET");
        string keyName = "airports.csv";

        const double timeoutDuration = 12;


        IAmazonS3 s3Client = new AmazonS3Client(RegionEndpoint.USEast1);
        string urlString = GeneratePresignedURL(s3Client, bucketName, keyName, timeoutDuration);
        Console.WriteLine($"The generated URL is: {urlString}.");
    }

    private static string GeneratePresignedURL(IAmazonS3 client, string bucketName, string objectKey, double duration)
    {
        string urlString = string.Empty;
        try
        {
            var request = new GetPreSignedUrlRequest()
            {
                BucketName = bucketName,
                Key = objectKey,
                Expires = DateTime.UtcNow.AddHours(duration),
            };
            urlString = client.GetPreSignedURL(request);
        }
        catch (AmazonS3Exception ex)
        {
            Console.WriteLine($"Error:'{ex.Message}'");
        }

        return urlString;
    }   
}
