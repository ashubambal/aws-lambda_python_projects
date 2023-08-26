import boto3

def lambda_handler(event, context):
    # Initialize the EC2 client
    ec2_client = boto3.client('ec2')
    instance_ids = set()
    # Describe instances that match the specified filters
    response = ec2_client.describe_instances(Filters=[
        {
        'Name': 'instance-state-name',
        'Values': ['running'],
        }
    ])

    for reservations in response['Reservations']:
        for instances in reservations['Instances']:
                instance_ids.add(instances['InstanceId'])
    
    # Stop each instance those status are running
    for each_instanceId in instance_ids:
        print(each_instanceId)
        stop_instances = ec2_client.stop_instances(
            InstanceIds=[each_instanceId])
        print(f"Stopping instance {each_instanceId}")

