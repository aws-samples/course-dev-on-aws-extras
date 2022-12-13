using Amazon.DynamoDBv2.DataModel;

namespace DynamoCrud;

[DynamoDBTable("Notes")]
public class Note
{
    [DynamoDBHashKey]
    public string UserId { get; set; }

    [DynamoDBRangeKey]
    public int NoteId { get; set; }

    [DynamoDBProperty("Note")]
    public string NoteString { get; set; }

    [DynamoDBProperty]
    public string Favorite { get; set; }

    public override string ToString()
    {
        return "Note [User=" + this.UserId + " , NoteId=" + this.NoteId + " , Note=" + this.NoteString + "]";
    }
}