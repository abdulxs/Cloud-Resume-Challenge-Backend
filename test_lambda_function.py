import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    @patch('lambda_function.boto3.resource')
    def test_get_visitor_count_success(self, mock_dynamodb_resource):
        # Mocking DynamoDB table and its get_item method
        mock_table = MagicMock()
        mock_table.get_item.return_value = {'Item': {'visitorCount': '1', 'count': 10}}
        mock_dynamodb_resource.return_value.Table.return_value = mock_table

        # Testing Lambda function for successful GET request
        event = {'httpMethod': 'GET'}
        response = lambda_handler(event, None)

        # Assertions
        mock_table.get_item.assert_called_once_with(Key={'visitorCount': '1'})
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {'visitorCount': 10})

    @patch('lambda_function.boto3.resource')
    def test_get_visitor_count_error(self, mock_dynamodb_resource):
        # Mocking DynamoDB table and causing an error in get_item method
        mock_table = MagicMock()
        mock_table.get_item.side_effect = Exception('Some error')
        mock_dynamodb_resource.return_value.Table.return_value = mock_table

        # Testing Lambda function for error in GET request
        event = {'httpMethod': 'GET'}
        response = lambda_handler(event, None)

        # Assertions
        mock_table.get_item.assert_called_once_with(Key={'visitorCount': '1'})
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error', json.loads(response['body']))

    @patch('lambda_function.boto3.resource')
    def test_update_visitor_count_success(self, mock_dynamodb_resource):
        # Mocking DynamoDB table and its update_item method
        mock_table = MagicMock()
        mock_table.update_item.return_value = {'Attributes': {'count': 11}}
        mock_dynamodb_resource.return_value.Table.return_value = mock_table

        # Testing Lambda function for successful POST request
        event = {'httpMethod': 'POST'}
        response = lambda_handler(event, None)

        # Assertions
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
        # Mocking DynamoDB table and causing an error in update_item method
        mock_table = MagicMock()
        mock_table.update_item.side_effect = Exception('Some error')
        mock_dynamodb_resource.return_value.Table.return_value = mock_table

        # Testing Lambda function for error in POST request
        event = {'httpMethod': 'POST'}
        response = lambda_handler(event, None)

        # Assertions
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
        # Testing Lambda function for an unsupported HTTP method
        event = {'httpMethod': 'PUT'}
        response = lambda_handler(event, None)

        # Assertions
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error', json.loads(response['body']))

if __name__ == '__main__':
    unittest.main()
