package software.amazon.samples.developingsamples.module5;

import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.CreateBucketRequest;

public class CreateBucket {

    public static void main(String[] args) {
        Region region = Region.AP_SOUTHEAST_2;

        S3Client s3 = S3Client.builder()
                .region(region)
                .credentialsProvider(ProfileCredentialsProvider.create("devdilt"))
                .build();

        CreateBucketRequest bucketRequest = CreateBucketRequest.builder()
                .bucket("russ-123-notes-bucket-java")
                .build();

        s3.createBucket(bucketRequest);
    }

}
