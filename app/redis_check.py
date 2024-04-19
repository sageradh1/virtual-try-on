import redis

redis_host = 'localhost'
redis_port = 6379
redis_db = 0

r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

response = r.ping()
if response:
    print("Redis is running and accessible.")
else:
    print("Failed to connect to Redis.")

print(r.ping())