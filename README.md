# Serverless Image Label Generator (AWS Rekognition + Lambda + API Gateway)

A serverless web app where users can upload an image and automatically get AI-generated labels with confidence scores using **Amazon Rekognition**.


## 🏗️ Architecture Overview

- **Frontend (HTML + JavaScript)**
  - Single page (index.html) with file upload, image preview, and "Analyze" button.
  - Sends image as base64 JSON to an API Gateway endpoint.

- **Amazon API Gateway (HTTP API)**
  - Public HTTPS endpoint (e.g. `/labels` route).
  - Forwards POST requests to Lambda.

- **AWS Lambda (Python)**
  - Receives base64 image from frontend.
  - Uses `boto3` to call `Rekognition.DetectLabels`.
  - Returns labels + confidence scores in JSON format.

- **Amazon S3**
  - Can host the frontend as a static website.
  - Can also be used later to store uploaded images.

- **CloudWatch**
  - Stores application logs from Lambda for debugging.

Region used: **ap-south-1 (Mumbai)**.

---

## 🧠 How It Works

1. User opens the web page and selects an image file.
2. Frontend converts the file to a base64 string and sends a POST request:

   ```json
   {
     "image": "<base64_string_here>"
   }
API Gateway routes the request to the Lambda function.

Lambda:

Decodes the base64 string into image bytes.

Calls:

rekognition.detect_labels(
  Image={'Bytes': body_bytes},
  MaxLabels=10,
  MinConfidence=70
)


Formats the response as:

{
  "labels": [
    { "name": "Person", "confidence": 99.12 },
    { "name": "Dog", "confidence": 95.33 }
  ]
}


Frontend displays the labels and confidence scores to the user.
