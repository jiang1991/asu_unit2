# This is a sample Python script.
import sys

import boto3
import logging
import os
from botocore.exceptions import ClientError
import time
import threading
from boto3.s3.transfer import TransferConfig

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

s3 = boto3.resource('s3')
ec2 = boto3.resource('ec2')

region = 'ap-northeast-2'
key = 'jiang'
key_filename = 'key_jiang.pem'
s3_bucket = 'jiang-s3-test'

file_dir = f'D:\\workspace\\py\\asu_unit2\\imagenet-100\\'


# create key
def create_key_pair(key_name, private_key_file_name=None):
    """
    Creates a key pair that can be used to securely connect to an Amazon EC2 instance.

    :param key_name: The name of the key pair to create.
    :param private_key_file_name: The file name where the private key portion of
                                  the newly created key is stored.
    :return: The newly created key pair.
    """
    try:
        key_pair = ec2.create_key_pair(KeyName=key_name)
        # logger.info("Created key %s.", key_pair.name)
        if private_key_file_name is not None:
            with open(private_key_file_name, 'w') as pk_file:
                # print(key_pair['KeyMaterial'])
                pk_file.write(key_pair.key_material)
            print(f"Wrote private key to {private_key_file_name}.")
    except ClientError:
        print(f"Couldn't create key {key_name}.")
        raise
    else:
        print(f'KEY:{key_name} created')
        return key_pair


# create ec2 resource
def create_ec2(image_id, instance_type, key_name, security_group_names=None):
    """
        Creates a new Amazon EC2 instance. The instance automatically starts immediately after
        it is created.

        The instance is created in the default VPC of the current account.

        :param image_id: The Amazon Machine Image (AMI) that defines the kind of
                         instance to create. The AMI defines things like the kind of
                         operating system, such as Amazon Linux, and how the instance is
                         stored, such as Elastic Block Storage (EBS).
        :param instance_type: The type of instance to create, such as 't2.micro'.
                              The instance type defines things like the number of CPUs and
                              the amount of memory.
        :param key_name: The name of the key pair that is used to secure connections to
                         the instance.
        :param security_group_names: A list of security groups that are used to grant
                                     access to the instance. When no security groups are
                                     specified, the default security group of the VPC
                                     is used.
        :return: The newly created instance.
        """
    try:
        instance_params = {
            'ImageId': image_id, 'InstanceType': instance_type, 'KeyName': key_name
        }
        if security_group_names is not None:
            instance_params['SecurityGroups'] = security_group_names
        instance = ec2.create_instances(**instance_params, MinCount=1, MaxCount=1)[0]
        # logger.info("Created instance %s.", instance.id)
        print(f'Created instance {instance.id}.')
    except ClientError:
        logging.exception(
            "Couldn't create instance with image %s, instance type %s, and key %s.",
            image_id, instance_type, key_name)
        raise
    else:
        return instance


# list ec2
def list_ec2():
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(instance.public_ip_address, instance.id)


# list s3
def list_s3():
    print('Buckets List:\n\t', *[b.name for b in s3.buckets.all()], sep="\n\t")


# create s3
def create_s3(bucket_name):
    try:
        print(f'\nCreating new bucket: {bucket_name}, wait until exists')
        bucket = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
    except ClientError as e:
        print(e)
        sys.exit('Exiting the script because bucket creation failed.')

    bucket.wait_until_exists()
    print(f'\nCreated new bucket: {bucket_name}.')
    list_s3()
    return bucket


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# s3 upload file
def upload_s3(des_dir, object_name=None):
    # Upload the file
    list_file = os.listdir(des_dir)

    for f in list_file:
        print(os.path.join(des_dir, f))
        s3.Bucket(s3_bucket).upload_file(
            os.path.join(des_dir, f),
            f
        )
        print(f'File: {f} uploaded to S3 bucket')