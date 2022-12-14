import boto3

# Resources represent an object-oriented interface to AWS. They provide a
# higher-level abstraction than the raw, low-level calls made by service clients
def list_resource():
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket('rrs-apps')
    for object in bucket.objects.all():
        print(object.key, object.last_modified)

list_resource()