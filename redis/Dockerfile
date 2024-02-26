# syntax=docker/dockerfile:1
# Build the application from source
FROM redis

EXPOSE 6379

COPY . .

CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]





