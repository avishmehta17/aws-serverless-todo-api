import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable')

def lambda_handler(event, context):
    print("Incoming event:", json.dumps(event))

    # Try query string parameter first
    task_id = None
    if event.get("queryStringParameters"):
        task_id = event["queryStringParameters"].get("id")

    # Fallback if testing via direct event
    if not task_id:
        task_id = event.get("id")

    if not task_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "taskId is required"})
        }

    table.delete_item(Key={'taskId': task_id})

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Task deleted", "deletedId": task_id})
    }
