import boto3

def get_volume_id_from_arn(volume_arn):

    # Split the ARN using the colon (":") seperator
    # volume_arn = "arn:aws:ec2:ap-south-1:371469041007:volume/vol-0103f474767d4b14c"
    arn_parts = volume_arn.split(':')

    # The volume ID is the last part of the ARN after 'volume/' prefix
    # output of above arn_parts = ['arn', 'aws', 'ec2', 'ap-south-1', '371469041007', 'volume/vol-0fbe270174df502ff']
    # Need to get last data element i.e "vol-0fbe270174df502ff" below is logic for that 
    volume_id = arn_parts[-1].split('/')[-1]

    # It will return volume id as "vol-06e0fcdbb1c8f4e20"
    return volume_id
    
def lambda_handler(event, context):
    
    # This will get the event log and it will sort out the volume arn
    volume_arn = event['resources'][0]

    # Using below function will get the exact volume_id 
    volume_id = get_volume_id_from_arn(volume_arn)

    # connect to the ec2 to modify the EBS volume
    ec2_client= boto3.client('ec2')
    response = ec2_client.modify_volume(
        VolumeId=volume_id,
        VolumeType='gp3',
    )