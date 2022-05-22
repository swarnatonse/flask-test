import boto3
import base64
import os
import json
import datetime
import pendulum
import string

dynamodb = boto3.client('dynamodb')
secretsmanager = boto3.client('secretsmanager')

def write_to_table(sleepdata):
    key = sleepdata['updatedate']
    if not key:
        print('Here')
        key = generate_ddb_key()
        
    dynamodb.put_item(
        TableName='SleepData', 
        Item={
            'DayId':{'S':key},
            'updatedate':{'S':sleepdata['updatedate']},
            'PhoneDownTime':{'S':sleepdata['phonedown']}, 
            'Activities':{'S':sleepdata['activities']},
            'Bedtime':{'S':sleepdata['bedtime']},
            'LightsOutTime':{'S':sleepdata['lightsout']},
            'WakeUpCount':{'S':sleepdata['howmanywakeup']},
            'WakeUpDuration':{'S':sleepdata['howlongawake']},
            'FinalWakeUpTime':{'S':sleepdata['wakeuptime']},
            'AriseTime':{'S':sleepdata['arisetime']},
            'LastUpdateTime':{'S': datetime.datetime.now().isoformat()}
        })
    
def generate_ddb_key():
    pst = pendulum.timezone('America/Los_Angeles')
    dt = datetime.datetime.now(pst)
    dt_string = dt.strftime("%Y-%m-%d")
    return dt_string
    
def get_login_info():
    get_secret_value_response = secretsmanager.get_secret_value(
            SecretId=os.environ.get('LOGIN_MANAGER')
        )
        
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        
    return json.loads(secret)
            
    