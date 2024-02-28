from functools import wraps
import logging
from flask import Flask, Response, request, jsonify
from prometheus_client import Counter, generate_latest, Summary, REGISTRY, CollectorRegistry, CONTENT_TYPE_LATEST
import redis

app = Flask(__name__)
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

# Configure logging
logging.basicConfig(filename='../api/app.log', level=logging.INFO)

# Define authentication tokens
AUTH_TOKENS = 'fo3cZ9EooJlwH7ubQ0I3CttqxE0SrzduMqbug0kfdKdoi0pUe5duwvwZ9R98oMvY'

REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint'])
REQUEST_LATENCY = Summary('request_latency_seconds', 'Request latency in seconds')

# Middleware for authentication
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        #Add here the desired validators        
        if auth_header == AUTH_TOKENS:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized access!'}), 401
    return wrapper

# Endpoint to collect metrics from pop, push and count endpoint
@app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    registry.register(REQUEST_COUNT)
    registry.register(REQUEST_LATENCY)
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

# Endpoint to pop data from Redis
@app.route('/api/queue/pop', methods=['POST'])
@authenticate
@REQUEST_LATENCY.time()
def pop_message():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    message = redis_db.lpop('message_queue')
    if message:
        logging.info('Message popped: %s', message.decode('utf-8'))
        return jsonify({'status': 'ok', 'message': message.decode('utf-8')}), 200
    else:
        logging.warning('No message found in the queue')
        return jsonify({'status': 'ok', 'message': None}), 200

# Endpoint to push data to Redis
@app.route('/api/queue/push', methods=['POST'])
@authenticate
@REQUEST_LATENCY.time()
def push_message():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    message = request.data.decode('utf-8')
    redis_db.rpush('message_queue', message)
    logging.info('Message pushed: %s', message)
    return jsonify({'status': 'ok'}), 200

# Endpoint to count data from Redis
@app.route('/api/queue/count', methods=['GET'])
@authenticate
@REQUEST_LATENCY.time()
def get_queue_count():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    count = redis_db.llen('message_queue')
    logging.info('Queue count retrieved: %s', count)
    return jsonify({'status': 'ok', 'count': count}), 200

# Endpoint to show logging info
@app.route('/log_file')
@authenticate
@REQUEST_LATENCY.time()
def view_log_file():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    logging.info('Queue count retrieved: %s', 'log_file_requested')
    
    # Define the path to the log file
    log_file_path = '../api/app.log'

    # Read the content of the log file
    with open(log_file_path, 'r') as file:
        log_content = file.read()

    # Return the log content as plain text
    return log_content, 200, {'Content-Type': 'text/plain'}

# Endpoint to get data from Redis
@app.route('/get/<key>', methods=['GET'])
def get_data(key):
    value = redis_db.get(key)
    if value:
        logging.info('Data retrieved for key %s: %s', key, value.decode('utf-8'))
        return jsonify({key: value.decode('utf-8')})
    else:
        logging.warning('Data not found for key %s', key)
        return jsonify({'error': 'Key not found!'}), 404
    
# Endpoint to add data in Redis
@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if key and value:
        redis_db.set(key, value)
        logging.info('Data added for key %s: %s', key, value)
        return jsonify({'message': 'Data added successfully!',
                      'status': 'OK!' })
    else:
        logging.error('Invalid key or value provided for adding data')
        return jsonify({'error': 'Invalid key or value provided!'}), 400
    
@app.route('/redis_health')
def health_check():
    try:
        # Check if Redis is reachable
        redis_db.ping()
        logging.info('Redis health check: Redis is up')
        return jsonify({'status': 'Redis is up'})
    except redis.exceptions.ConnectionError:
        logging.error('Redis health check: Redis is down')
        return jsonify({'status': 'Redis is down'}), 500

if __name__ == '__main__':
    app.run(debug=True)
