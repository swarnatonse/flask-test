import boto3
import datetime
import pendulum
import random
import string

dynamodb = boto3.client('dynamodb')

def write_to_table():
    key = generate_ddb_key()
    dynamodb.put_item(TableName='SleepData', Item={'DayId':{'S':key},'key2':{'S':''.join(random.choices(string.ascii_lowercase, k=5))}})
    
def generate_ddb_key():
    pst = pendulum.timezone('America/Los_Angeles')
    dt = datetime.datetime.now(pst)
    dt_string = dt.strftime("%Y-%m-%d")
    return dt_string