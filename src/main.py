import json

def lambda_handler(event, context):
    """
    Main Lambda handler function.
    """
    print("Lambda function invoked!")
    print("Event: ", event)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from your Social Media Scheduler Lambda!')
    }
