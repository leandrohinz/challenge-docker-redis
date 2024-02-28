Challenge - Docker + Redis + API
LEANDRO HINESTROZA - HALO

*******************************
In the folder api you'll find:

- The dockerfile with the different steps of the base image used, the install of the dependencies, the ports and the flask app run commands.

Stage 1 (builder): This stage installs dependencies specified in requirements.txt to create a build environment. It uses the python:3.9 base image.

Stage 2 (final): This stage starts from a lighter base image (python:3.9-slim) to reduce the image size. It copies only the installed dependencies from the previous stage into the final image, along with your application code.

Dependencies and application code are copied separately to avoid copying unnecessary build dependencies into the final image.

--no-cache-dir flag is used with pip install to avoid caching the downloaded packages, reducing the final image size.

--from=builder specifies to copy files from the builder stage.

- The main.py file, this is the main python + flask app, the app consist of:
- Configuration of logging: this one collects all logs to the file app.log
Logging statements using logging.info, logging.warning, and logging.error are added at various points in the code to log relevant information, such as when messages are pushed or popped from the queue, when data is retrieved or added to Redis, and during Redis health checks.
The logging.basicConfig call configures logging to write to a file named app.log and sets the logging level to INFO, so all levels of logs (info, warning, error) will be captured.

- The definition of the auth token used, in this case is : fo3cZ9EooJlwH7ubQ0I3CttqxE0SrzduMqbug0kfdKdoi0pUe5duwvwZ9R98oMvY

- The middleware for the authentication: The authenticate function is a middleware that checks if the request contains a valid authorization token in the Authorization header. If the token is valid, the request proceeds to the endpoint; otherwise, it returns a 401 Unauthorized error.

The @authenticate decorator is applied to each endpoint that requires authentication.

- The endpoint to collect metrics from pop, push and count endpoint, this endpoint shows number of request count, request latency in seconds and app request count

Route:

@app.route('/api/queue/pop', methods=['POST']): This decorator defines the URL endpoint for this function. In this case, it's set to /api/queue/pop, and it specifies that it should respond to HTTP POST requests.

Authentication:

@authenticate: This custom decorator is applied to the function for the auth. 

Request Latency Monitoring:

@REQUEST_LATENCY.time(): This decorator indicates that the duration of the request will be measured. It's used for monitoring the latency of requests.
Endpoint Function:

def pop_message():: This is the function that gets executed when a POST request is made to /api/queue/pop.
Metrics Collection:

REQUEST_COUNT.labels(request.method, request.path).inc(): This line uses  metrics library (Prometheus) to track request counts, methods, and paths.

Redis Interaction:

message = redis_db.lpop('message_queue'): This line retrieves and removes the leftmost (first) item from the Redis list named 'message_queue'. It's assumed that redis_db is an instance of a Redis client, enabling interaction with a Redis database.

Response Handling:

After attempting to pop a message from the Redis queue, the function checks if a message was retrieved. If a message exists, it logs the message and returns a JSON response with status 'ok' and the popped message.
If no message is found, it logs a warning and returns a JSON response with status 'ok' and a None value for the message.

- The endpoint to pop data from redis: This Flask endpoint is designed to handle a POST request to pop data from a Redis queue, this endpoint essentially provides an API for popping messages from a Redis queue, along with appropriate logging and monitoring of request metrics.

Keep in mind this one works like the previous one but the redis operation is different: 

Redis Interaction:

redis_db.rpush('message_queue', message): This line pushes the decoded message onto the right end of the Redis list named 'message_queue'. It assumes that redis_db is an instance of a Redis client, allowing interaction with a Redis database.

- The endpoint to count the data from redis: This Flask endpoint is designed to handle a GET request to count the number of items in a Redis queue

Keep in mind this one works like the previous one but the redis operation is different: 

Redis Interaction:

count = redis_db.llen('message_queue'): This line retrieves the length of the Redis list named 'message_queue', which effectively gives the count of items in the queue. It assumes that redis_db is an instance of a Redis client, allowing interaction with a Redis database.

- The endpoint to show logging info from a file: Is designed to handle a GET request to view the content of a log file (app.log)


**********************************
In the folder tests, you'll find:

The file test_api.py, To test the API endpoints and Redis functionality for our  Flask project we used a testing framework called pytest

Each test function sends requests to the corresponding API endpoints and checks the response status code and body for correctness

***********************************
Commands:

You can run the hole proyect using the docker-compose.yml file in the root folder with this command:

docker compose up

Optional commands/troubleshooting, if theres any dependence with problems you can run these commands to install the dependencies manually:

pip install pytest
pip install Flask redis
sudo apt install prometheus

**************************************
API TEST

POSTMAN TEST
You can test the API endpoints using tools like cURL or Postman. For example:

To push a message: curl -X POST -d "Message1" http://localhost:5000/api/queue/push
To pop a message: curl -X POST http://localhost:5000/api/queue/pop
To get the count of messages: curl http://localhost:5000/api/queue/count
To get the metrics: curl http://localhost:5000/metrics
To get the logs: curl http://localhost:5000/logs

Dont forget to add the header Key: Content-Type, Value: application/json and Key: Authorization, Value: fo3cZ9EooJlwH7ubQ0I3CttqxE0SrzduMqbug0kfdKdoi0pUe5duwvwZ9R98oMvY to get the correct response from the API in postman.

PYTEST:
To run the endpoint api tests you can run the file test_api.py located in the folder tests with this command: pytest

****************************************
