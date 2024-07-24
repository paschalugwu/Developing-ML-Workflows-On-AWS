import json
import boto3
import base64

# Initialize a low-level client representing Amazon Simple Storage Service (S3)
s3_client = boto3.client('s3')

# Initialize a low-level client representing Amazon SageMaker Runtime
runtime_client = boto3.client('sagemaker-runtime')

# Name of the deployed model endpoint
ENDPOINT = "image-classification-2024-07-23-22-21-09-444"

# Threshold for filtering inferences
THRESHOLD = 0.70


def serialize_image_data(event, context):
    """
    A function to serialize target data from S3.

    Parameters:
    event (dict): The event dictionary containing the S3 bucket and key.
    context (LambdaContext): The context in which the Lambda function is called.

    Returns:
    dict: A dictionary containing the serialized image data and other relevant information.
    """
    print("Received event:", event)

    # Get the s3 address from the Step Function event input
    key = event.get('s3_key')
    bucket = event.get('s3_bucket')

    if not key or not bucket:
        return {
            'statusCode': 400,
            'error': 'Missing s3_key or s3_bucket in the event'
        }

    # Download the data from s3 to /tmp/image.png
    s3_client.download_file(bucket, key, "/tmp/image.png")

    # Read and encode the data from the file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    print("Event:", event.keys())

    return {
        'statusCode': 200,
        'body': json.dumps({
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        })
    }


def classify_image(event, context):
    """
    A function to classify the image using SageMaker endpoint.

    Parameters:
    event (dict): The event dictionary containing the image data.
    context (LambdaContext): The context in which the Lambda function is called.

    Returns:
    dict: A dictionary containing the classification results.
    """
    try:
        print("Received event:", event)

        # Decode the image data
        image_data = event.get('image_data')
        if not image_data:
            return {
                'statusCode': 400,
                'error': "Missing 'image_data' in the event"
            }

        image = base64.b64decode(image_data)

        # Invoke the SageMaker endpoint
        response = runtime_client.invoke_endpoint(
            EndpointName=ENDPOINT,
            Body=image,
            ContentType='image/png'
        )

        # Extract inferences from the response
        inferences = json.loads(response['Body'].read().decode('utf-8'))

        # Add inferences to the event
        event['inferences'] = inferences
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        return {
            'statusCode': 400,
            'error': f"Missing key: {str(e)}"
        }
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'error': str(e)
        }


def filter_inferences(event, context):
    """
    A function to filter inferences based on a confidence threshold.

    Parameters:
    event (dict): The event dictionary containing the inferences.
    context (LambdaContext): The context in which the Lambda function is called.

    Returns:
    dict: A dictionary containing the filtered results.
    """
    print("Event received:", event)

    try:
        # Extract inferences from the event
        inferences = event.get('inferences', [])
        if not inferences and 'body' in event:
            body = event['body']
            if isinstance(body, str):
                body = json.loads(body)
            inferences = body.get('inferences', [])

        print("Inferences found:", inferences)

        # Check if any values in our inferences are above THRESHOLD
        meets_threshold = max(inferences) > THRESHOLD

        if meets_threshold:
            print("Inference meets the threshold.")
        else:
            raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

        return {
            'statusCode': 200,
            'body': event
        }
    except KeyError as e:
        print(f"KeyError: {str(e)}")
        return {
            'statusCode': 400,
            'error': f"Missing key: {str(e)}"
        }
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'error': str(e)
        }
