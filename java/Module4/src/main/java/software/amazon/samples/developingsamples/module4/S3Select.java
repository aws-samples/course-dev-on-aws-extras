package software.amazon.samples.developingsamples.module4;

import software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider;
import software.amazon.awssdk.core.async.SdkPublisher;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3AsyncClient;
import software.amazon.awssdk.services.s3.model.*;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;

public class S3Select {
    public static void main(String[] args) {
        ProfileCredentialsProvider credentialsProvider = ProfileCredentialsProvider.create();
        Region region = Region.US_EAST_1;
        S3AsyncClient s3 = S3AsyncClient.builder()
                .region(region)
                .credentialsProvider(credentialsProvider)
                .build();

        String bucketName = System.getenv("MY_BUCKET");
        String keyName = "airports.csv";

        selectContentFromObject(s3,bucketName,keyName);
    }

    public static void selectContentFromObject(S3AsyncClient s3, String bucketName, String keyName) {
        InputSerialization inputSerialization = InputSerialization.builder()
                .csv(CSVInput.builder().fileHeaderInfo("Use").build())
                .build();

        OutputSerialization outputSerialization = OutputSerialization.builder()
                .csv(CSVOutput.builder().build())
                .build();

        SelectObjectContentRequest request = SelectObjectContentRequest.builder()
                .bucket(bucketName)
                .key(keyName)
                .expressionType("SQL")
                .expression("select * from s3object s where s.\"iso_country\" like '%US%'")
                .inputSerialization(inputSerialization)
                .outputSerialization(outputSerialization)
                .build();

        ResponseHandler responseHandler = new ResponseHandler();

        try {
            s3.selectObjectContent(request, responseHandler).get();
        } catch (InterruptedException | ExecutionException e) {
            System.out.println("Error: " + e.getMessage());
        }

        RecordsEvent response = (RecordsEvent) responseHandler.receivedEvents.stream()
                .filter(e -> e.sdkEventType() == SelectObjectContentEventStream.EventType.RECORDS)
                .findFirst()
                .orElse(null);

        System.out.println(response.payload().asUtf8String());

    }

    private static class ResponseHandler implements SelectObjectContentResponseHandler {
        private SelectObjectContentResponse response;
        private List<SelectObjectContentEventStream> receivedEvents = new ArrayList<>();
        private Throwable exception;

        @Override
        public void responseReceived(SelectObjectContentResponse response) {
            this.response = response;
        }

        @Override
        public void onEventStream(SdkPublisher<SelectObjectContentEventStream> publisher) {
            publisher.subscribe(receivedEvents::add);
        }

        @Override
        public void exceptionOccurred(Throwable throwable) {
            exception = throwable;
        }

        @Override
        public void complete() {
        }
    }

}

