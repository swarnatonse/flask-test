import requests
import json
from aws_requests_auth.aws_auth import AWSRequestsAuth

def create_request(credentials, endpoint, data):
    auth = AWSRequestsAuth(aws_access_key=credentials.access_key,
                       aws_secret_access_key=credentials.secret_key,
                       aws_host=endpoint,
                       aws_region='us-east-1',
                       aws_service='lambda')

    response = requests.post('https://' + endpoint + '/',
                                auth=auth,
                                data=json.dumps(data))
    return response