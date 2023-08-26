import boto3

def lambda_handler(event, context):
    # Establish connection with EC2 client
    ec2_client = boto3.client('ec2')
    instance_ids = set()
    
    # List down all the instance those were in stopped status
    response = ec2_client.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['stopped']
        },
        {
            'Name':'tag:env',
            'Values':['dev','stg']
        }
    ])
    for reservations in response['Reservations']:
        for instances in reservations['Instances']:
            instance_ids.add(instances['InstanceId'])
            
    for each_instanceid in instance_ids:
        start_response = ec2_client.start_instances(InstanceIds=[each_instanceid])
        print(f"Instances Started :{start_response}")
