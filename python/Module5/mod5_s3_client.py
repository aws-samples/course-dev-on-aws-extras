import boto3

# Create S3 resource using custom session
session = boto3.session.Session(profile_name='staging')

# Retrieve region from session object
current_region = session.region_name

# Create a high-level resource from custom session
resource = session.resource('s3')
bucket = resource.Bucket('notes-bucket')

# Region-specific endpoints require the LocationConstraint parameter
bucket.create(
    CreateBucketConfiguration={
        'LocationConstraint': current_region
    }
)
