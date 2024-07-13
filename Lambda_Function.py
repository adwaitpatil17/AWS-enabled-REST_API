import json
import boto3
import time
import os
s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']
def lambda_handler (event, context):
    print(event)
    http_method = event['httpMethod']
    if http_method == "POST":
        return create_device(event)
    elif http_method == "GET":
        if event.get('queryStringParameters') and 'device_id' in event['queryStringParameters']:
            return get_device(event)
        else:
            return get_all_devices(event)
    elif http_method == "PUT":
        return update_device(event)
    elif http_method == "DELETE":
        return delete_device(event)
    else:
        return {
            'statusCode' : 202,
            'body' : json.dumps("Work in Progress") 
        }
    
    
def create_device(event):
    payload = json.loads(event['body'])
    device_id = payload['device_id'] 
    s3.put_object(                                     # function of boto3 
        Bucket = BUCKET_NAME,
        #Key = str(device_id) + "_" + str(time.time()),   #key here is filename0
        Key = str(device_id),
        Body = json.dumps(payload)
    )
    return {
        'statusCode' : 201,
        'body' : json.dumps("device Created Successfully")
    }

def get_device(event):
    device_id = event['queryStringParameters']['device_id']
    try:
        get_device_details = s3.get_object(
            Bucket = BUCKET_NAME,
            Key = device_id
            )
        device_data = get_device_details['Body'].read().decode('utf-8')
        return{
           'statusCode' : 200,
           'body' : device_data
           }  
        
    except s3.exceptions.NoSuchKey as e:
        print(f"{device_id} doesn't exist")
        return{
            'statusCode' : 404,
            'body' : json.dumps("device doesn't exist")
        }

def get_all_devices(event):
    list_devices = s3.list_objects_v2(Bucket=BUCKET_NAME)
    devices = list_devices.get('Contents', [])    #list of objects else [] 'Contains' is a key in the response
    all_devices = []                           #that contains a list of objects in the bucket
    for device in devices:
        device_id = device['Key']
        try: 
            get_device_details = s3.get_object(
            Bucket = BUCKET_NAME,
            Key = device_id
        )
            device_data = get_device_details['Body'].read().decode('utf-8')
            all_devices.append(json.loads(device_data))
            
        
        except Exception as e:
            print(f"Error fetching with device with ID {device_id} : {str(e)}")
            continue
    return{
        'statusCode' : 200,
        'body' : json.dumps(all_devices)
    }
        

def update_device(event):
     payload = json.loads(event['body'])
     device_id = payload['device_id'] 
     s3.put_object(                                     # function of boto3 
        Bucket = BUCKET_NAME,
        #Key = str(device_id) + "_" + str(time.time()),   #key here is filename0
        Key = str(device_id),
        Body = json.dumps(payload)
    )
     return {
        'statusCode' : 200,
        'body' : json.dumps("Device details Updated Successfully")
    }
    

def delete_device(event):
    device_id = event['queryStringParameters']['device_id']
    try:
        s3.delete_object(
            Bucket = BUCKET_NAME,
            Key = device_id
            )
        return {
            'statusCode' : 200,
            'body' : json.dumps("Device details Deleted Successfully")  
            }
    except Exception as e:
        return {
            'statusCode' : 500,
            'body' : json.dumps("Error deleting device details")
            }
        