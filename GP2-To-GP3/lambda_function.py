import boto3

def get_volume_id_from_arn(volume_arn):
    # Split the ARN using the colon (":") separator
    arn_parts = volume_arn.split(':')

    # The volume ID is the last part of the ARN after the 'volume/' prefix
    # Example output of arn_parts: ['arn', 'aws', 'ec2', 'ap-south-1', '371469041007', 'volume/vol-0fbe270174df502ff']
    # Extracting the last data element, i.e., "vol-0fbe270174df502ff"
    volume_id = arn_parts[-1].split('/')[-1]

    # It will return the volume ID as "vol-06e0fcdbb1c8f4e20"
    return volume_id
    
def lambda_handler(event, context):
    # Extract the volume ARN from the event log
    volume_arn = event['resources'][0]

    # Using the function below will retrieve the exact volume ID
    volume_id = get_volume_id_from_arn(volume_arn)

    # Connect to EC2 to modify the EBS volume
    ec2_client = boto3.client('ec2')
    response = ec2_client.modify_volume(
        VolumeId=volume_id,
        VolumeType='gp3',
    )

    return {
        'statusCode': 200,
        'body': 'Volume type modified to gp3 successfully.'
    }
