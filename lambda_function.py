import json
import boto3

AWS_REGION = 'eu-north-1'

dynamodb = boto3.resource('dynamodb',region_name=AWS_REGION)
table = dynamodb.Table('Resume')  # Replace with your actual table name

def lambda_handler(event, context):
    if isinstance(event, list):  # Check if it's an array
        # Process each event in the array
        responses = [process_single_event(e) for e in event]
        return responses
    else:
        # Process a single event
        return process_single_event(event)

def process_single_event(event):
    # Get method (retrieve visitor count)
    if event.get('httpMethod') == 'GET':
        try:
            response = table.get_item(
                Key={'visitorCount': '1'}  # Update the key here
            )
            item = response.get('Item', {})
            count = item.get('count', 0)
            count = float(count)
            return {
                'statusCode': 200,
                'body': json.dumps({'visitorCount': count})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    # Post method (update visitor count)
    elif event.get('httpMethod') == 'POST':
        try:
            response = table.update_item(
                Key={'visitorCount': '1'},  # Update the key here
                UpdateExpression='SET #count = #count + :incr',
                ExpressionAttributeNames={'#count': 'count'},
                ExpressionAttributeValues={':incr': 1},
                ReturnValues='UPDATED_NEW'
            )
            updated_count = response.get('Attributes', {}).get('count', 0)
            updated_count = float(updated_count)
            return {
                'statusCode': 200,
                'body': json.dumps({'updatedVisitorCount': updated_count})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    # Handle unsupported methods
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Unsupported method', 'receivedMethod': event.get('httpMethod')})
        }
