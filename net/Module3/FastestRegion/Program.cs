using System.Diagnostics;
using Amazon;
using Amazon.EC2;

namespace FastestRegion;
class Program
{
    static async Task Main(string[] args)
    {
        AmazonEC2Client[] clients = {
                new AmazonEC2Client(RegionEndpoint.USEast1),
                new AmazonEC2Client(RegionEndpoint.USEast2),
                new AmazonEC2Client(RegionEndpoint.USWest1),
                new AmazonEC2Client(RegionEndpoint.USWest2),
                new AmazonEC2Client(RegionEndpoint.APNortheast1),
                new AmazonEC2Client(RegionEndpoint.APNortheast2),
                new AmazonEC2Client(RegionEndpoint.APNortheast3),
                new AmazonEC2Client(RegionEndpoint.APSouth1),
                new AmazonEC2Client(RegionEndpoint.APSoutheast1),
                new AmazonEC2Client(RegionEndpoint.APSoutheast2),
            };

        var tasks = clients.Select(async client =>
        {
            var task1watch = new Stopwatch();
            task1watch.Start();
            var t = await client.DescribeRegionsAsync();
            Console.WriteLine($" {client.Config.RegionEndpoint}  {task1watch.ElapsedMilliseconds}");
            return t;
        });
        var results = await Task.WhenAll(tasks);

    }
}
