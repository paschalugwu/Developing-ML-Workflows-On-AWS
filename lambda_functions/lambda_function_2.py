import json
import base64
import boto3

# Using low-level client representing Amazon SageMaker Runtime (To invoke endpoint)
runtime_client = boto3.client('sagemaker-runtime')                   

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2024-07-23-22-21-09-444" ## TODO: fill in (Trained IC Model Name)

def lambda_handler(event, context):
    try:
        # Print the event for debugging
        print("Received event:", event)

        # Decode the image data
        image_data = event.get('image_data')
        if not image_data:
            return {
                'statusCode': 400,
                'error': "Missing 'image_data' in the event"
            }
        
        image = base64.b64decode(image_data)     # Decoding the encoded 'Base64' image-data and class remains 'bytes'

        # Instantiate a Predictor (Here we have renamed 'Predictor' to 'response')
        # Response after invoking a deployed endpoint via SageMaker Runtime 
        response = runtime_client.invoke_endpoint(
                                            EndpointName=ENDPOINT,    # Endpoint Name
                                            Body=image,               # Decoded Image Data as Input (class: 'Bytes') Image Data
                                            ContentType='image/png'   # Type of inference input data - Content type (Eliminates the need of serializer)
                                        )

        # Make a prediction: Unpack response
        # (NOTE: 'response' returns a dictionary with inferences in the "Body" : (StreamingBody needs to be read) having Content_type='string')
        inferences = json.loads(response['Body'].read().decode('utf-8'))     # list

        # We return the data back to the Step Function    
        event['inferences'] = inferences            # List of predictions               
        return {
            'statusCode': 200,
            'body': json.dumps(event)               # Passing the event python dictionary in the body
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
