import boto3
import base64
import os
import json
import datetime
import pendulum
import string

dynamodb = boto3.client('dynamodb')
secretsmanager = boto3.client('secretsmanager')
s3 = boto3.client('s3')
session = boto3.Session()

form_input_map = {
    'updatedate': 'updatedate',
    'phonedown': 'PhoneDownTime',
    'activities': 'Activities',
    'bedtime': 'Bedtime',
    'lightsout': 'LightsOutTime',
    'howlongtillasleep': 'HowLongToSleep',
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
    item = construct_ddb_item(sleepdata)
    dynamodb.put_item(
        TableName='SleepData', 
        Item=item
    )

def update_table(sleepdata):
    item = construct_update_item(sleepdata)
    dynamodb.update_item(
        TableName='SleepData',
        Key=item['Key'],
        UpdateExpression=item['UpdateExpression'],
        ExpressionAttributeValues=item['ExpressionAttributeValues']
    )
        
def get_item_from_table(date):
    return dynamodb.get_item(
        TableName='SleepData', 
        Key={
            'DayId': { 'S' : date }
        })
    
def generate_ddb_key():
    pst = pendulum.timezone('America/Los_Angeles')
    dt = datetime.datetime.now(pst)
    dt_string = dt.strftime("%Y-%m-%d")
    return dt_string
    
def construct_ddb_item(sleepdata):
    itemkey = sleepdata['updatedate']
    if not itemkey:
        itemkey = generate_ddb_key()
        
    ddb_item = {}
    ddb_item['DayId'] = { 'S': itemkey }
    for key, value in form_input_map.items():
        attr = sleepdata.get(key)
        if attr:
            ddb_item[value] = { 'S': attr }
            
    ddb_item['LastUpdateTime'] = {'S': datetime.datetime.now().isoformat()}
    
    return ddb_item
    
def construct_update_item(sleepdata):
    itemkey = sleepdata['updatedate']
    if not itemkey:
        itemkey = generate_ddb_key()
    ddb_item_key = dict()
    ddb_item_key['DayId'] = { 'S': itemkey }
    
    update_expression = 'SET '
    exp_attr_values = dict()
    for key, value in form_input_map.items():
        attr = sleepdata.get(key)
        if attr:
            update_expression = update_expression + value + ' = :' + key + ', '
            exp_attr_values[':' + key] = { 'S' : attr }
            
    update_expression = update_expression + 'LastUpdateTime = :lut'
    exp_attr_values[':lut'] = { 'S': datetime.datetime.now().isoformat() }
    
    update_item = dict()
    update_item['Key'] = ddb_item_key
    update_item['UpdateExpression'] = update_expression
    update_item['ExpressionAttributeValues'] = exp_attr_values
    
    return update_item
    
def get_sleepdata(date):
    result = get_item_from_table(date)
    if result.get('Item'):
        dateddbitem = result.get('Item')
        sleepdata = dict()
        for key, value in form_input_map.items():
            if dateddbitem.get(value):
                sleepdata[key] = dateddbitem[value]['S']
            else:
                sleepdata[key] = None
    else:
        sleepdata = None

    return sleepdata
    
    
def get_login_info():
    get_secret_value_response = secretsmanager.get_secret_value(
            SecretId=os.environ.get('LOGIN_MANAGER')
        )
        
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        
    return json.loads(secret)
         
def get_report_file(report_key):
    bucket_name = os.environ.get('S3_BUCKET')
    s3.download_file(bucket_name, 'reports/' + report_key, report_key)
    return report_key
         
def get_report_lambda_url():
    return os.environ.get('REPORT_LAMBDA_URL')
    
def get_credentials():
    credentials = session.get_credentials()
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    
    return credentials