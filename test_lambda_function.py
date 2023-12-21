import json
import boto3
import unittest
from lambda_function import lambda_handler

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('Resume')  # Replace with your actual table name

class TestLambdaHandler(unittest.TestCase):
    def test_get_method(self):
        event = {
            "httpMethod": "GET"
        }
        response = lambda_handler(event, None)
        print(response)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], json.dumps({'visitorCount': 1}))

    def test_post_method(self):
        event = {
            "httpMethod": "POST"
        }
        response = lambda_handler(event, None)
        print(response) 
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], json.dumps({'updatedVisitorCount': 2}))

    def test_invalid_method(self):
        event = {
            "httpMethod": "PUT"
        }
        response = lambda_handler(event, None)
        print(response) 
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['body'], json.dumps({'error': 'Unsupported method', 'receivedMethod': 'PUT'}))

    def test_array_of_events(self):
        event = [
            {'httpMethod': 'GET'},
            {'httpMethod': 'POST'}
        ]
        responses = lambda_handler(event, None)
        print(responses) 
        self.assertEqual(len(responses), 2)
        self.assertEqual(responses[0]['statusCode'], 200)
        self.assertEqual(responses[0]['body'], json.dumps({'visitorCount': 1}))
        self.assertEqual(responses[1]['statusCode'], 200)
        self.assertEqual(responses[1]['body'], json.dumps({'updatedVisitorCount': 2}))

if __name__ == '__main__':
    unittest.main()
