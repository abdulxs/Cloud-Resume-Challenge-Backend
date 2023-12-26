import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler

class TestLambdaIntegration(unittest.TestCase):
    def setUp(self):
        # Create a mock DynamoDB table
        self.mock_table = MagicMock()
        patcher = patch('lambda_function.boto3.resource')
        self.mock_dynamodb_resource = patcher.start()
        self.mock_dynamodb_resource.return_value.Table.return_value = self.mock_table
        self.addCleanup(patcher.stop)

    def test_get_visitor_count_success(self):
        # Configure the mock to return data for a successful DynamoDB query
        self.mock_table.get_item.return_value = {'Item': {'visitorCount': '1', 'count': 10}}

        # Construct the event for the GET and POST method
        event = [{
            'httpMethod': 'GET',
            'headers': {'Host': 'https://6kk5qw05q5.execute-api.eu-north-1.amazonaws.com/development/resumeFunction'},
            'queryStringParameters': None,
            'body': None,
            'isBase64Encoded': False
        },
                 {
      "httpMethod": "POST",
      "headers": {
        "Host": "https://6kk5qw05q5.execute-api.eu-north-1.amazonaws.com/development/resumeFunction"
      },
      "body": "{\"visitorCount\": \"1\", \"count\": 1}",
      'isBase64Encoded': False
    }]

        # Call the lambda_handler function
        response = lambda_handler(event, None)

        # Assertions
        self.mock_table.get_item.assert_called_once_with(Key={'visitorCount': '1'})
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {'visitorCount': 10})

if __name__ == '__main__':
    unittest.main()
