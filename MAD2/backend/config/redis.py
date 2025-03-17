import redis
import json

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Create Redis Index (Run Once)
# def create_redis_index():
#     try:
#         # Attempt to get index info (if it exists)
#         redis_client.execute_command('FT.INFO', 'idx')
#         print("Index already exists.")
#     except redis.exceptions.ResponseError as e:
#         # If the index does not exist, create it
#         if "Unknown Index name" in str(e):
#             redis_client.execute_command(
#                 'FT.CREATE', 'idx',
#                 'ON', 'JSON',
#                 'PREFIX', '1', 'service:',
#                 'SCHEMA',
#                 '$.service_name', 'AS', 'service_name', 'TEXT',
#                 '$.status', 'AS', 'status', 'TAG'
#             )
#             print("Index created successfully.")
#         else:
#             print(f"Error creating index: {e}")

# # Call the function when the app starts
# create_redis_index()
