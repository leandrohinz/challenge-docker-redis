import pytest
import requests
import json
import redis

# Flask app is running on localhost:5000
BASE_URL = 'http://localhost:5000'

# Redis server is running on localhost:6379
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Initialize Redis connection
redis_db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# Helper function to clear Redis queue before each test
def clear_redis_queue():
    redis_db.delete('message_queue')

# Fixture to set up and tear down Redis queue for each test
@pytest.fixture(autouse=True)
def setup_teardown():
    clear_redis_queue()
    yield
    clear_redis_queue()

# Test for pop endpoint
def test_pop_message():
    # Push a message to Redis queue
    redis_db.rpush('message_queue', 'test_message')

    # Make a POST request to pop endpoint
    response = requests.post(f'{BASE_URL}/api/queue/pop')

    # Check response status code
    assert response.status_code == 200

    # Check response body
    data = response.json()
    assert data['status'] == 'ok'
    assert data['message'] == 'test_message'

# Test for push endpoint
def test_push_message():
    # Make a POST request to push endpoint
    response = requests.post(f'{BASE_URL}/api/queue/push', data='test_value', headers={'Content-Type': 'application/json'})

    # Check response status code
    assert response.status_code == 200

    # Check Redis queue for pushed message
    message = redis_db.lpop('message_queue')
    assert message.decode('utf-8') == 'test_value'

# Test for count endpoint
def test_get_queue_count():
    # Push three messages to Redis queue
    redis_db.rpush('message_queue', 'message1', 'message2', 'message3')

    # Make a GET request to count endpoint
    response = requests.get(f'{BASE_URL}/api/queue/count')

    # Check response status code
    assert response.status_code == 200

    # Check response body
    data = response.json()
    assert data['status'] == 'ok'
    assert data['count'] == 3
