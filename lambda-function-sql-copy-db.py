import boto3  
import botocore  
import datetime  
import re  
import logging
region='us-east-1'  
db_instance_class='db.m3.medium'  
db_subnet='ll-vpc subnets'  
instances = ['sql-ll']
db_id = 'dev-sql-ll'
print('Loading function')
def byTimestamp(snap):  
  if 'SnapshotCreateTime' in snap:
    return datetime.datetime.isoformat(snap['SnapshotCreateTime'])
  else:
    return datetime.datetime.isoformat(datetime.datetime.now())
def lambda_handler(event, context):  
    source = boto3.client('rds', region_name=region)
    for instance in instances:
      try:
        source_snaps = source.describe_db_snapshots(DBInstanceIdentifier = instance)['DBSnapshots']
        #print "DB_Snapshots:", source_snaps
        source_snap = sorted(source_snaps, key=byTimestamp, reverse=True)[0]['DBSnapshotIdentifier']
        print('Will restore %s to %s' % (source_snap, db_id))
        response = source.restore_db_instance_from_db_snapshot(DBInstanceIdentifier=db_id, DBSnapshotIdentifier=source_snap, DBInstanceClass=db_instance_class, DBSubnetGroupName=db_subnet,MultiAZ=False,PubliclyAccessible=False,StorageType='gp2',OptionGroupName='ll-sqlserver-2012',AvailabilityZone='us-east-1c')
        print(response)
      except botocore.exceptions.ClientError as e:
        raise Exception("Could not restore: %s" % e)
