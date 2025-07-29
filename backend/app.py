import json
import boto3
import os
from datetime import datetime
from uuid import uuid4

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    method = event["httpMethod"]

    if method == "POST":
        data = json.loads(event["body"])
        feedback = {
            "id": str(uuid4()),
            "name": data.get("name"),
            "message": data.get("message"),
            "timestamp": datetime.utcnow().isoformat()
        }
        table.put_item(Item=feedback)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Feedback submitted!"})
        }

    elif method == "GET":
        items = table.scan()["Items"]
        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }

    else:
        return {"statusCode": 405, "body": "Method not allowed"}