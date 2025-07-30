import json
import boto3
from datetime import datetime
from uuid import uuid4

# Hardcoded DynamoDB table name
TABLE_NAME = "FeedbackTable"

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    method = event["httpMethod"]
    
    if method == "POST":
        # Parse feedback data from request
        try:
            data = json.loads(event["body"])
            feedback = {
                "id": str(uuid4()),
                "name": data.get("name"),
                "message": data.get("message"),
                "timestamp": datetime.utcnow().isoformat()
            }

            # Store to DynamoDB
            table.put_item(Item=feedback)

            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Feedback submitted!"}),
                "headers": {"Content-Type": "application/json"}
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)}),
                "headers": {"Content-Type": "application/json"}
            }

    elif method == "GET":
        # Retrieve all feedbacks (for admin route)
        try:
            response = table.scan()
            items = response.get("Items", [])

            return {
                "statusCode": 200,
                "body": json.dumps(items),
                "headers": {"Content-Type": "application/json"}
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)}),
                "headers": {"Content-Type": "application/json"}
            }

    else:
        return {
            "statusCode": 405,
            "body": json.dumps({"message": "Method not allowed"}),
            "headers": {"Content-Type": "application/json"}
        }
