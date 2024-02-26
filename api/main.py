from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
redis_db = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

@app.route('/api/queue/pop', methods=['POST'])
def popmessage():
    message = redis_db.lpop('message_queue')
    if message:
        return jsonify({'status': 'ok', 'message': message.decode('utf-8')}), 200
    else:
        return jsonify({'status': 'ok', 'message': None}), 200

@app.route('/api/queue/push', methods=['POST'])
def push_message():
    message = request.data.decode('utf-8')
    redis_db.rpush('message_queue', message)
    return jsonify({'status': 'ok'}), 200

@app.route('/api/queue/count', methods=['GET'])
def get_queue_count():
    count = redis_db.llen('message_queue')
    return jsonify({'status': 'ok', 'count': count}), 200

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

# Endpoint to get data from Redis
@app.route('/get/<key>', methods=['GET'])
def get_data(key):
    value = redis_db.get(key)
    if value:
        return jsonify({key: value.decode('utf-8')})
    else:
        return jsonify({'error': 'Key not found!'}), 404
    

if __name__ == '__main__':
    app.run(debug=True)





