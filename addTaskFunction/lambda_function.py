import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable')

def lambda_handler(event, context):
    # Print the event so we can see what API Gateway is sending
    print("Incoming event:", json.dumps(event))

    # 1️⃣ Try to get the body safely
    if 'body' in event and event['body']:
        # This is the case when API Gateway sends {"body": "...json string..."}
        try:
            body = json.loads(event['body'])
        except (TypeError, json.JSONDecodeError):
            # If body is already a dict or something odd
            if isinstance(event['body'], dict):
                body = event['body']
            else:
                body = {}
    else:
        # 2️⃣ Fallback: sometimes, when using the Test tool,
        # the JSON you enter is passed directly as the event (no "body" key)
        body = event

    # 3️⃣ Get taskName from the parsed body
    task_name = body.get('taskName')

    if not task_name:
        # If taskName is missing, return a clear error
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "taskName is required in the request body",
                "received_body": body
            })
        }

    # 4️⃣ Create the item to store in DynamoDB
    task_id = str(uuid.uuid4())
    created_at = str(datetime.utcnow())

    table.put_item(
        Item={
            'taskId': task_id,
            'taskName': task_name,
            'createdAt': created_at
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Task added",
            "taskId": task_id
        })
    }
