import json
import boto3

client = boto3.client('iot-data', region_name='us-west-1')

def lambda_handler(event, context):
    print(event)
    # TODO implement
    # Change topic, qos and payload
    response = client.publish(
        topic=event["headers"]["device"]+"/"+event["headers"]["topic"],
        qos=1,
        payload=json.dumps(json.loads(event["headers"]["data"]))
    )
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Published to topic')
    }