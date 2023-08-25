import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get the IAM user's AWS account ID
    account_id = boto3.client('sts').get_caller_identity().get('Account')

    # Get all EBS Snapshots owned by the user
    response = ec2.describe_snapshots(OwnerIds=[account_id])

    # Iterate through each snapshot and delete if it's not attached to any volume and not associated with any instance
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')
        
        # Get the list of attachments associated with the snapshot
        attachments = snapshot.get('Attachments', [])

        # Delete the snapshot only if both volume_id and attachments are empty
        if not volume_id and not attachments:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume and not associated with any instance.")
        else:
            # Check if the volume still exists
            try:
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                if not volume_response['Volumes'][0]['Attachments']:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot {snapshot_id} as it was taken from a volume not attached to any running instance.")
            except ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    # The volume associated with the snapshot is not found (it might have been deleted)
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot {snapshot_id} as its associated volume was not found.")
