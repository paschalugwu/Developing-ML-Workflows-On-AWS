import json
import boto3
import base64

# A low-level client representing Amazon Simple Storage Service (S3)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Print the event for debugging
    print("Received event:", event)
    
    # Get the s3 address from the Step Function event input (You may also check lambda test)
    key = event.get('s3_key')  # Use get method to avoid KeyError
    bucket = event.get('s3_bucket')  # Use get method to avoid KeyError
    
    if not key or not bucket:
        return {
            'statusCode': 400,
            'error': 'Missing s3_key or s3_bucket in the event'
        }
    
    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, "/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:  # Read binary file
        image_data = base64.b64encode(f.read()).decode('utf-8')  # Base64 encode binary data and decode to string

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            "image_data": image_data,  # Encoded data as string
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        })
    }
