import json
import boto3
import unittest

dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('Resume')  # Replace with your actual table name

def test_lambda_handler_get_method():
    event = json.dumps({
        "httpMethod": "GET"
    })
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert response['body'] == json.dumps({'visitorCount': 1})

def test_lambda_handler_post_method():
    event = json.dumps({
        "httpMethod": "POST"
    })
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    assert response['body'] == json.dumps({'updatedVisitorCount': 2})

def test_lambda_handler_invalid_method():
    event = json.dumps({
        "httpMethod": "PUT"
    })
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
    assert response['body'] == json.dumps({'error': 'Unsupported method', 'receivedMethod': 'PUT'})

def test_lambda_handler_array_of_events():
    event = json.dumps([
        {'httpMethod': 'GET'},
        {'httpMethod': 'POST'}
    ])
    responses = lambda_handler(event, None)
    assert len(responses) == 2
    assert responses[0]['statusCode'] == 200
    assert responses[0]['body'] == json.dumps({'visitorCount': 1})
    assert responses[1]['statusCode'] == 200
    assert responses[1]['body'] == json.dumps({'updatedVisitorCount': 2})

if __name__ == '__main__':
    unittest.main()
