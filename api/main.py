from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
redis_db = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

# Sample endpoint to set data in Redis
@app.route('/set', methods=['POST'])
def set_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if key and value:
        redis_db.set(key, value)
        return jsonify({'message': 'Data set successfully!'})
    else:
        return jsonify({'error': 'Invalid key or value provided!'}), 400
    
# Sample endpoint to set data in Redis
@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if key and value:
        redis_db.set(key, value)
        return jsonify({'message': 'Data added successfully!'})
    else:
        return jsonify({'error': 'Invalid key or value provided!'}), 400

# Sample endpoint to set data in Redis
@app.route('/pop', methods=['POST'])
def pop_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if key and value:
        redis_db.set(key, value)
        return jsonify({'message': 'Data added successfully!',
                      'status': 'OK!' })
    else:
        return jsonify({'error': 'Invalid key or value provided!'}), 200

# Sample endpoint to get data from Redis
@app.route('/get/<key>', methods=['GET'])
def get_data(key):
    value = redis_db.get(key)
    if value:
        return jsonify({key: value.decode('utf-8')})
    else:
        return jsonify({'error': 'Key not found!'}), 404
    
# Sample endpoint to set data in Redis
@app.route('/prueba', methods=['GET'])
def prueba():
    return jsonify({'message': 'Data get successfully!'})

if __name__ == '__main__':
    app.run(debug=True)




