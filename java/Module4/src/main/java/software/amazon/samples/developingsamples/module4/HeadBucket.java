package software.amazon.samples.developingsamples.module4;

import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
import software.amazon.awssdk.awscore.exception.AwsServiceException;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.HeadBucketRequest;
import software.amazon.awssdk.services.s3.model.HeadBucketResponse;

public class HeadBucket {

    public static void main(String[] args) {
        ProfileCredentialsProvider credentialsProvider = ProfileCredentialsProvider.create();
        Region region = Region.US_EAST_1;
        S3Client s3 = S3Client.builder()
                .region(region)
                .credentialsProvider(credentialsProvider)
                .build();

        bucketExisting(s3, "<bucket name here>");
        s3.close();

    }

    private static boolean bucketExisting(S3Client s3, String bucketName) {
        boolean exists = false;
        try {
            HeadBucketRequest request = HeadBucketRequest.builder().bucket(bucketName).build();
            HeadBucketResponse result = s3.headBucket(request);
            if (result.sdkHttpResponse().statusCode() == 200) {
                System.out.println("Bucket exists!");
                exists = true;
            }

        } catch (AwsServiceException awsEx) {
            switch(awsEx.statusCode()) {
                case 404:
                    System.out.println("No such bucket existing");
                case 400:
                    System.out.println("Attempted to access a bucket from a Region other than where it exists");
                case 403:
                    System.out.println("Permission errors in accessing bucket");
            }
        }
        return exists;
    }
}
