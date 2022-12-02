using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.DataModel;
using Amazon.DynamoDBv2.DocumentModel;

namespace DynamoCrud;
class Program
{
    static async Task Main(string[] args)
    {
        var client = new AmazonDynamoDBClient();
        DynamoDBContext context = new DynamoDBContext(client);

        await RetrieveNote(context);
        await AddNote(context);
        await RetrieveNote(context);
        await DisplayFavoriteNotesForUser(context);
    }

    private static async Task AddNote(DynamoDBContext context)
    {
        Note noteToAdd = new Note {
            UserId = "StudentA",
            NoteId = 55,
            NoteString = "This is a note I am adding.",
            Favorite = "Yes"
        };
        await context.SaveAsync(noteToAdd);
    }

    private static async Task DisplayFavoriteNotesForUser(DynamoDBContext context)
    {
        var results = await context.QueryAsync<Note>("StudentA", new DynamoDBOperationConfig {
            QueryFilter = new List<ScanCondition>() { new ScanCondition("Favorite", ScanOperator.Equal, "Yes") }
        }).GetRemainingAsync();

        results.ForEach(Console.WriteLine);
    }

    private static async Task<Note> RetrieveNote(DynamoDBContext context)
    {
        Note note = await context.LoadAsync<Note>("StudentA", 55);
        if (note != null) {
            Console.WriteLine("****** The note reads: " + note.NoteString);
        }
        return note;
    }
}
