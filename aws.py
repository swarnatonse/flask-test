import boto3
import base64
import os
import json
import datetime
import pendulum
import string

dynamodb = boto3.client('dynamodb')
secretsmanager = boto3.client('secretsmanager')

form_input_map = {
    'updatedate': 'updatedate',
    'phonedown': 'PhoneDownTime',
    'activities': 'Activities',
    'bedtime': 'Bedtime',
    'lightsout': 'LightsOutTime',
    'howmanywakeup': 'WakeUpCount',
    'howlongawake': 'WakeUpDuration',
    'wakeuptime': 'FinalWakeUpTime',
    'arisetime': 'AriseTime',
    'sleepnotes': 'SleepNotes',
    'fitbithrs': 'FitbitHours',
    'fitbitmins': 'FitbitMins',
    'fitbitscore': 'FitbitScore',
    'exercisetime': 'ExerciseTime',
    'exercises': 'Exercises',
    'stress': 'Stress',
    'mood': 'Mood',
    'energy1': 'MorningEnergy',
    'energy2': 'ForenoonEnergy',
    'energy3': 'AfternoonEnergy',
    'energy4': 'EveningEnergy'
}

def write_to_table(sleepdata):
    itemkey = sleepdata['updatedate']
    if not itemkey:
        itemkey = generate_ddb_key()
        
    item = {}
    item['DayId'] = { 'S': itemkey }
    for key, value in form_input_map.items():
        attr = sleepdata.get(key)
        item[value] = { 'S': attr if attr else '' }
            
    item['LastUpdateTime'] = {'S': datetime.datetime.now().isoformat()}
        
    dynamodb.put_item(
        TableName='SleepData', 
        Item=item
    )
        
def get_item_from_table(date):
    return dynamodb.get_item(
        TableName='SleepData', 
        Key={
            'DayId': {'S':date}
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
            
    