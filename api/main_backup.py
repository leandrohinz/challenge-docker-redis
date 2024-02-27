from flask import Flask, Response, request, jsonify
#from flask_basicauth import BasicAuth
from prometheus_client import Counter, generate_latest, Summary, REGISTRY, CollectorRegistry, CONTENT_TYPE_LATEST
import redis

app = Flask(__name__)
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

# Configurar las credenciales para la autenticación básica
#app.config['BASIC_AUTH_USERNAME'] = 'username'
#app.config['BASIC_AUTH_PASSWORD'] = 'password'

# Inicializar la extensión de autenticación básica
#basic_auth = BasicAuth(app)

# Función de autenticación para verificar las credenciales
#@basic_auth.check_credentials
# def check_credentials(username, password):
#     # Verificar las credenciales del usuario
#     return username == app.config['BASIC_AUTH_USERNAME'] and password == app.config['BASIC_AUTH_PASSWORD']

REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint'])
REQUEST_LATENCY = Summary('request_latency_seconds', 'Request latency in seconds')

# Endpoint to metrics from pop,push and count endpoint
@app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    registry.register(REQUEST_COUNT)
    registry.register(REQUEST_LATENCY)
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

# Endpoint to pop data from Redis
@app.route('/api/queue/pop', methods=['POST'])
@REQUEST_LATENCY.time()
#@basic_auth.required
def pop_message():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    message = redis_db.lpop('message_queue')
    if message:
        return jsonify({'status': 'ok', 'message': message.decode('utf-8')}), 200
    else:
        return jsonify({'status': 'ok', 'message': None}), 200

# Endpoint to push data to Redis
@app.route('/api/queue/push', methods=['POST'])
@REQUEST_LATENCY.time()
#@basic_auth.required
def push_message():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    message = request.data.decode('utf-8')
    redis_db.rpush('message_queue', message)
    return jsonify({'status': 'ok'}), 200

# Endpoint to count data from Redis
@app.route('/api/queue/count', methods=['GET'])
@REQUEST_LATENCY.time()
#@basic_auth.required
def get_queue_count():
    REQUEST_COUNT.labels(request.method, request.path).inc()
    count = redis_db.llen('message_queue')
    return jsonify({'status': 'ok', 'count': count}), 200

# Endpoint to get data from Redis
@app.route('/get/<key>', methods=['GET'])
def get_data(key):
    value = redis_db.get(key)
    if value:
        return jsonify({key: value.decode('utf-8')})
    else:
        return jsonify({'error': 'Key not found!'}), 404
    
# Endpoint to add data in Redis
@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if key and value:
        redis_db.set(key, value)
        return jsonify({'message': 'Data added successfully!',
                      'status': 'OK!' })
    else:
        return jsonify({'error': 'Invalid key or value provided!'}), 400
    
@app.route('/redis_health')
def health_check():
    try:
        # Check if Redis is reachable
        redis_db.ping()
        return jsonify({'status': 'Redis is up'})
    except redis.exceptions.ConnectionError:
        return jsonify({'status': 'Redis is down'}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Endpoint to POP data in Redis
# @app.route('/api/queue/pop', methods=['POST'])
# def pop_data():
#     data = request.get_json()
#     key = data.get('key')
#     value = data.get('value')
#     if key and value:
#         redis_db.set(key, value)
#         return jsonify({'message': 'Data added successfully!',
#                       'status': 'OK!' })
#     else:
#         return jsonify({'error': 'Invalid key or value provided!'}), 200
    
#  # Endpoint to PUSH data in Redis
# @app.route('/api/queue/push', methods=['POST'])
# def push_data():
#     data = request.get_json()
#     key = data.get('key')
#     value = data.get('value')
#     if key and value:
#         redis_db.set(key, value)
#         return jsonify({'message': 'Data added successfully!',
#                       'status': 'OK!' })
#     else:
#         return jsonify({'error': 'Invalid key or value provided!'}), 200   
    
#  # Endpoint to COUNT data in Redis
# @app.route('/api/queue/count', methods=['GET'])
# def count_data():
#     data = request.get_json()
#     key = data.get('key')
#     value = data.get('value')
#     if key and value:
#         redis_db.get(key, value)
#         return jsonify({'count': 'Data count obtained successfully!',
#                       'status': 'OK!' })
#     else:
#         return jsonify({'error': 'Invalid key or value provided!'}), 200   




