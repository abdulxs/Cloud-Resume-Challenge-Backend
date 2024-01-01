import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler


class TestLambdaIntegration(unittest.TestCase):
    @patch('lambda_function.boto3.resource')
    def test_event_passing(self, mock_dynamodb_resource):
        # Mock the DynamoDB resource
        mock_table = mock_dynamodb_resource.return_value.Table.return_value

        # Construct a sample event
        event = {
            'httpMethod': 'GET',
            'headers': {'Host': 'https://exampleHost.com'},
            'queryStringParameters': None,
            'body': None
        }

        # Call the lambda_handler with the sample event
        lambda_handler(event, None)

        # Assert that the lambda_handler was called with the expected event
        mock_table.get_item.assert_not_called()  # No get_item call for this event

if __name__ == '__main__':
    unittest.main()
