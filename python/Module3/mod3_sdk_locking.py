# see a list of API versions here: https://github.com/boto/botocore/tree/master/botocore/data
import boto3

versions = ["2014-09-01",
"2014-10-01",
"2015-03-01",
"2015-04-15",
"2015-10-01",
"2016-04-01",
"2016-09-15",
"2016-11-15"]

def paths(obj):
    all_paths = []
    add_paths(all_paths, obj, "")
    return set(all_paths)

def add_paths(all_paths, obj, crumbs):
    if not isinstance(obj, dict):
        return

    for key in obj.keys():
        path = crumbs + key
        all_paths.append(path)
        add_paths(all_paths, obj[key], path + " > ")

prev_paths = None
for version in versions:
    ec2 = boto3.client("ec2", api_version=version)
    result = ec2.describe_instances()
    current_paths = paths(result["Reservations"][0]["Instances"][0])
    if prev_paths:
        new_keys = sorted(list(current_paths-prev_paths))
        if new_keys:
            print(f"DescribeInstance version {version}")
            print("New keys:")
            for key in new_keys:
                print(" "+ key)
            print()
    prev_paths = current_paths
