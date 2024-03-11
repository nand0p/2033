from pprint import pprint
import boto3
import json


debug=False
prefix='scores/'
bucket='2030.hex7.com'
scores_list_name='scores_list.json'


scores_list = []
client = boto3.client("s3", region_name='us-east-1')

response = client.list_objects_v2(Bucket=bucket,
                                  Prefix=prefix,
                                  Delimiter='/')

if debug:
  pprint(response)

if 'Contents' not in response:
  raise Exception('response not valid: ', response)
else:
  for key in response['Contents']:
    scores_list.append(key['Key'])

pprint(scores_list)

response = client.put_object(ACL='public-read',
                             Body=json.dumps(scores_list),
                             Bucket=bucket,
                             Key='scores_list.json')

if debug:
  pprint(response)
