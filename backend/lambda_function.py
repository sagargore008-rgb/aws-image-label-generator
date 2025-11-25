import json
import base64
import boto3

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    try:
        # Log some of the event to debug
        print("EVENT (truncated):", json.dumps(event)[:500])

        # 1. Get body as string
        body_str = event.get("body")
        if not body_str:
            return _response(400, {"error": "Empty request body"})

        # 2. Parse JSON body
        # For HTTP API, body is a JSON string
        if isinstance(body_str, dict):
            body = body_str
        else:
            body = json.loads(body_str)

        # 3. Get base64 image string
        image_b64 = body.get("image")
        if not image_b64:
            return _response(400, {"error": "Missing 'image' field in request"})

        # 4. Decode base64 into raw image bytes
        try:
            image_bytes = base64.b64decode(image_b64)
        except Exception as e:
            print("Base64 decode error:", repr(e))
            return _response(400, {"error": "Invalid base64 image data"})

        print("Decoded image bytes length:", len(image_bytes))

        # 5. Call Rekognition
        rekog_response = rekognition.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=70
        )

        labels = [
            {
                "name": lbl["Name"],
                "confidence": round(lbl["Confidence"], 2)
            }
            for lbl in rekog_response.get("Labels", [])
        ]

        return _response(200, {"labels": labels})

    except Exception as e:
        print("ERROR in lambda_handler:", repr(e))
        return _response(500, {"error": "Internal server error"})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }
