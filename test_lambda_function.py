import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    @patch('lambda_function.boto3.resource')
    def test_get_visitor_count_success(self, mock_dynamodb_resource):
        mock_table = MagicMock()
        mock_dynamodb_resource.return_value.Table.return_value = mock_table
        mock_table.get_item.return_value = {'Item': {'visitorCount': '1', 'count': 10}}

        # Construct the event for the GET method
        event = {
            'httpMethod': 'GET',
            'headers': {
                'Host': 'https://6kk5qw05q5.execute-api.eu-north-1.amazonaws.com/development/resumeFunction'
            },
            'queryStringParameters': None,
            'body': None,
            'isBase64Encoded': False
        }

        response = lambda_handler(event, None)

        mock_table.get_item.assert_called_once_with(Key={'visitorCount': '1'})
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {'visitorCount': 10})

    @patch('lambda_function.boto3.resource')
    def test_get_visitor_count_error(self, mock_dynamodb_resource):
        mock_table = MagicMock()
        mock_dynamodb_resource.return_value.Table.return_value = mock_table
        mock_table.get_item.side_effect = Exception('Some error')

        # Construct the event for the GET method
        event = {
            'httpMethod': 'GET',
            'headers': {
                'Host': 'https://6kk5qw05q5.execute-api.eu-north-1.amazonaws.com/development/resumeFunction'
            },
            'queryStringParameters': None,
            'body': None,
            'isBase64Encoded': False
        }

        response = lambda_handler(event, None)

        mock_table.get_item.assert_called_once_with(Key={'visitorCount': '1'})
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error', json.loads(response['body']))

    @patch('lambda_function.boto3.resource')
    def test_update_visitor_count_success(self, mock_dynamodb_resource):
        mock_table = MagicMock()
        mock_dynamodb_resource.return_value.Table.return_value = mock_table
        mock_table.update_item.return_value = {'Attributes': {'count': 11}}

        # Construct the event for the POST method
        event = {
            'httpMethod': 'POST',
            'headers': {
                'Host': 'https://6kk5qw05q5.execute-api.eu-north-1.amazonaws.com/development/resumeFunction'
            },
            'queryStringParameters': None,
            'body': None,
            'isBase64Encoded': False
        }

        response = lambda_handler(event, None)

        mock_table.update_item.assert_called_once_with(
            Key={'visitorCount': '1'},
            UpdateExpression='SET #count = #count + :incr',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':incr': 1},
            ReturnValues='UPDATED_NEW'
        )
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {'updatedVisitorCount': 11})

    @patch('lambda_function.boto3.resource')
    def test_update_visitor_count_error(self, mock_dynamodb_resource):
        mock_table = MagicMock()
        mock_dynamodb_resource.return_value.Table.return_value = mock_table
        mock_table.update_item.side_effect = Exception('Some error')

        # Construct the event for the POST method
        event = {
            'httpMethod': 'POST',
            'headers': {
                'Host': 'https://6kk5qw05q5.execute-api.eu-north-1.amazonaws.com/development/resumeFunction'
            },
            'queryStringParameters': None,
            'body': None,
            'isBase64Encoded': False
        }

        response = lambda_handler(event, None)

        mock_table.update_item.assert_called_once_with(
            Key={'visitorCount': '1'},
            UpdateExpression='SET #count = #count + :incr',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':incr': 1},
            ReturnValues='UPDATED_NEW'
        )
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error', json.loads(response['body']))

    @patch('lambda_function.boto3.resource')
    def test_unsupported_method(self, mock_dynamodb_resource):
        # Construct the event for an unsupported method
        event = {
            'httpMethod': 'PUT',
            'headers': {
                'Host': 'https://6kk5qw05q5.execute-api.eu-north-1.amazonaws.com/development/resumeFunction'
            },
            'queryStringParameters': None,
            'body': None,
            'isBase64Encoded': False
        }

        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error', json.loads(response['body']))

if __name__ == '__main__':
    unittest.main()
