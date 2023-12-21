import json
import unittest
from unittest.mock import patch
from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    @patch('boto3.resource')
    def test_get_visitor_count_success(self, mock_dynamodb_resource):
        mock_table = mock_dynamodb_resource.return_value.Table.return_value
        mock_table.get_item.return_value = {'Item': {'visitorCount': '1', 'count': 10}}

        # Test with a single event
        single_event = {'httpMethod': 'GET'}
        response = lambda_handler(single_event, None)

        mock_table.get_item.assert_called_once_with(Key={'visitorCount': '1'})
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {'visitorCount': 10})

        # Reset the mock for the next test
        mock_table.reset_mock()

        # Test with multiple events
        multiple_events = [{'httpMethod': 'GET'}, {'httpMethod': 'GET'}]
        response = lambda_handler(multiple_events, None)

        # Verify that the mock was called for each event in the array
        mock_table.get_item.assert_called_with(Key={'visitorCount': '1'})
        self.assertEqual(mock_table.get_item.call_count, 2)

    @patch('boto3.resource')
    def test_get_visitor_count_error(self, mock_dynamodb_resource):
        mock_table = mock_dynamodb_resource.return_value.Table.return_value
        mock_table.get_item.side_effect = Exception('Some error')

        # Test with a single event
        single_event = {'httpMethod': 'GET'}
        response = lambda_handler(single_event, None)

        mock_table.get_item.assert_called_once_with(Key={'visitorCount': '1'})
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error', json.loads(response['body']))

        # Reset the mock for the next test
        mock_table.reset_mock()

        # Test with multiple events
        multiple_events = [{'httpMethod': 'GET'}, {'httpMethod': 'GET'}]
        response = lambda_handler(multiple_events, None)

        # Verify that the mock was called for each event in the array
        mock_table.get_item.assert_called_with(Key={'visitorCount': '1'})
        self.assertEqual(mock_table.get_item.call_count, 2)

    @patch('boto3.resource')
    def test_update_visitor_count_success(self, mock_dynamodb_resource):
        mock_table = mock_dynamodb_resource.return_value.Table.return_value
        mock_table.update_item.return_value = {'Attributes': {'count': 11}}

        # Test with a single event
        single_event = {'httpMethod': 'POST'}
        response = lambda_handler(single_event, None)

        mock_table.update_item.assert_called_once_with(
            Key={'visitorCount': '1'},
            UpdateExpression='SET #count = #count + :incr',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':incr': 1},
            ReturnValues='UPDATED_NEW'
        )
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {'updatedVisitorCount': 11})

        # Reset the mock for the next test
        mock_table.reset_mock()

        # Test with multiple events
        multiple_events = [{'httpMethod': 'POST'}, {'httpMethod': 'POST'}]
        response = lambda_handler(multiple_events, None)

        # Verify that the mock was called for each event in the array
        mock_table.update_item.assert_called_with(
            Key={'visitorCount': '1'},
            UpdateExpression='SET #count = #count + :incr',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':incr': 1},
            ReturnValues='UPDATED_NEW'
        )
        self.assertEqual(mock_table.update_item.call_count, 2)

    @patch('boto3.resource')
    def test_update_visitor_count_error(self, mock_dynamodb_resource):
        mock_table = mock_dynamodb_resource.return_value.Table.return_value
        mock_table.update_item.side_effect = Exception('Some error')

        # Test with a single event
        single_event = {'httpMethod': 'POST'}
        response = lambda_handler(single_event, None)

        mock_table.update_item.assert_called_once_with(
            Key={'visitorCount': '1'},
            UpdateExpression='SET #count = #count + :incr',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':incr': 1},
            ReturnValues='UPDATED_NEW'
        )
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('error', json.loads(response['body']))

        # Reset the mock for the next test
        mock_table.reset_mock()

        # Test with multiple events
        multiple_events = [{'httpMethod': 'POST'}, {'httpMethod': 'POST'}]
        response = lambda_handler(multiple_events, None)

        # Verify that the mock was called for each event in the array
        mock_table.update_item.assert_called_with(
            Key={'visitorCount': '1'},
            UpdateExpression='SET #count = #count + :incr',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':incr': 1},
            ReturnValues='UPDATED_NEW'
        )
        self.assertEqual(mock_table.update_item.call_count, 2)

    # Add similar adjustments for other test methods...

if __name__ == '__main__':
    unittest.main()
