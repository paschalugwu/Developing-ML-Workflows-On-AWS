import json

THRESHOLD = 0.70

def lambda_handler(event, context):
    print("Event received: ", event)  # Debugging print statement

    try:
        # Try to extract inferences from the top level of the event
        if 'inferences' in event:
            inferences = event['inferences']
        else:
            # If not found, try to extract inferences from the body
            if 'body' in event:
                body = event['body']
                if isinstance(body, str):
                    body = json.loads(body)
                if 'inferences' in body:
                    inferences = body['inferences']
                else:
                    print("Body content:", body)  # Debugging print statement
                    raise KeyError("Missing 'inferences' key in body")
            else:
                print("Event content:", event)  # Debugging print statement
                raise KeyError("Missing 'inferences' key in event")

        print("Inferences found: ", inferences)  # Debugging print statement

        # Check if any values in our inferences are above THRESHOLD
        meets_threshold = max(inferences) > THRESHOLD

        # If our threshold is met, pass our data back out of the
        # Step Function, else, end the Step Function with an error
        if meets_threshold:
            print("Inference meets the threshold.")  # Debugging print statement
        else:
            raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

        return {
            'statusCode': 200,
            'body': event  # Passing the final event as a dictionary
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
