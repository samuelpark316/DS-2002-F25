import boto3
import requests

bucket = 'ds2002-f25-skj9vk'
object_name = 'cat_spin.gif'
expires_in = 604800  # 7 days

# Fetch from internet
url = "https://media.tenor.com/2g4B_5Q4U8YAAAAC/cat-spin.gif"
data = requests.get(url).content

with open(object_name, 'wb') as f:
    f.write(data)

s3 = boto3.client('s3', region_name='us-east-1')

# Upload
s3.upload_file(object_name, bucket, object_name)

# Presign
presigned = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': object_name},
    ExpiresIn=expires_in
)

print("Presigned URL:")
print(presigned)