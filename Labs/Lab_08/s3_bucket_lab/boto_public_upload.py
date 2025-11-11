import boto3

s3 = boto3.client('s3', region_name='us-east-1')
bucket = 'ds2002-f25-sjp6fe'
file_path = 'google_logo.png'

with open(file_path, 'rb') as f:
    s3.put_object(
        Body=f,
        Bucket=bucket,
        Key='google_logo_public.png',
        ACL='public-read'
    )

print("Uploaded public file.")