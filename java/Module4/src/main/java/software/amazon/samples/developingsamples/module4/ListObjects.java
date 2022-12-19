package software.amazon.samples.developingsamples.module4;

import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.ListObjectsV2Request;
import software.amazon.awssdk.services.s3.paginators.ListObjectsV2Iterable;

public class ListObjects {
    public static void main(String[] args) {
        ProfileCredentialsProvider credentialsProvider = ProfileCredentialsProvider.create();
        Region region = Region.US_EAST_1;
        S3Client s3 = S3Client.builder()
                .region(region)
                .credentialsProvider(credentialsProvider)
                .build();

        String bucketName = System.getenv("MY_BUCKET");

        printObjects(s3, buildRequest(bucketName));
    }

    private static ListObjectsV2Request buildRequest(String bucketName) {
        return ListObjectsV2Request.builder()
                .bucket(bucketName).maxKeys(2).build();
    }

    private static void printObjects(S3Client s3, ListObjectsV2Request request) {
        ListObjectsV2Iterable objects = s3.listObjectsV2Paginator(request);

        objects.stream().flatMap(r -> r.contents().stream())
                .forEach(content -> System.out.println("Key : " + content.key()));
    }
}
