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

region = 'ap-northeast-2'
key = 'jiang'
key_filename = 'key_jiang.pem'
s3_bucket = 'jiang-s3-test'

file_dir = f'D:\\workspace\\py\\asu_unit2\\imagenet-100\\'


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
def upload_s3(dir, object_name=None):
    # Upload the file
    list_file = os.listdir(dir)

    for f in list_file:
        print(os.path.join(dir, f))
        s3.Bucket(s3_bucket).upload_file(
            os.path.join(dir, f),
            f
        )
        print(f'File: {f} uploaded to S3 bucket')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_s3(s3_bucket)
    upload_s3(file_dir)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
