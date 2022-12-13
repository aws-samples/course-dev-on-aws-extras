package software.amazon.samples.developingsamples.module8;

import software.amazon.awssdk.enhanced.dynamodb.*;
import software.amazon.awssdk.enhanced.dynamodb.model.GetItemEnhancedRequest;
import software.amazon.awssdk.enhanced.dynamodb.model.PageIterable;
import software.amazon.awssdk.enhanced.dynamodb.model.QueryConditional;
import software.amazon.awssdk.enhanced.dynamodb.model.QueryEnhancedRequest;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.DynamoDbException;

import java.util.HashMap;
import java.util.Map;


public class NoteCRUD {
    public static void main(String[] args) {
        DynamoDbClient ddb = DynamoDbClient.builder()
                .region(Region.US_EAST_1)
                .build();

        DynamoDbEnhancedClient enhancedClient = DynamoDbEnhancedClient.builder()
                .dynamoDbClient(ddb)
                .build();


        retrieveNote(enhancedClient);
        addNote(enhancedClient);
        retrieveNote(enhancedClient);
        displayFavoriteNotesForUser(enhancedClient);
    }

    public static void addNote(DynamoDbEnhancedClient enhancedClient) {
        try {
            DynamoDbTable table = enhancedClient.table("Notes", TableSchema.fromBean(Note.class));

            Note noteToAdd = new Note();
            noteToAdd.setUserId("StudentA");
            noteToAdd.setNoteId(55);
            noteToAdd.setNote("This is a note I am adding.");

            table.putItem(noteToAdd);
        } catch(DynamoDbException e) {
            System.err.println(e.getMessage());
        }
    }

    public static void deleteNote() {
        // Challenge: Complete this method using the enhanced client
    }

    public static void displayFavoriteNotesForUser(DynamoDbEnhancedClient enhancedClient) {
        DynamoDbTable table = enhancedClient.table("Notes", TableSchema.fromBean(Note.class));
        int countFavoriteNotes = 0;

        AttributeValue attributeValue = AttributeValue.builder()
                .s("Yes")
                .build();

        Map<String, AttributeValue> expressionValues = new HashMap<>();
        expressionValues.put(":value", attributeValue);

        Expression expression = Expression.builder()
                .expression("Favorite = :value")
                .expressionValues(expressionValues)
                .build();

        QueryConditional queryConditional = QueryConditional
            .keyEqualTo(Key.builder().partitionValue("StudentA")
            .build());

        PageIterable results = table.query(QueryEnhancedRequest.builder().queryConditional(queryConditional).filterExpression(expression).build());

        results.items().forEach(System.out::println);
    }

    public static Note retrieveNote(DynamoDbEnhancedClient enhancedClient) {
        Note result = null;

        try{
            DynamoDbTable<Note> table = enhancedClient.table("Notes", TableSchema.fromBean(Note.class));
            Key key = Key.builder()
                    .partitionValue("StudentD").sortValue((Number)42)
                    .build();

            result = table.getItem(
                    (GetItemEnhancedRequest.Builder requestBuilder) -> requestBuilder.key(key));
            System.out.println("****** The note reads: " + result.getNote());
        } catch (DynamoDbException e) {
            System.err.println(e.getMessage());
        }
        return result;
    }
}
