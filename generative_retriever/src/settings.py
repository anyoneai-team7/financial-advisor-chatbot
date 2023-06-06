<<<<<<< HEAD
from pathlib import Path
import os

=======
import os

API_KEY = os.getenv("OPENAI_API_KEY")

>>>>>>> ciro
# REDIS
# Queue name
REDIS_QUEUE = "service_queue"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0
# Host IP
<<<<<<< HEAD
REDIS_IP = "localhost"
# Sleep parameters which manages the
# interval between requests to our redis queue
SERVER_SLEEP = 0.05
=======
REDIS_IP = "redis"
# Sleep parameters which manages the
# interval between requests to our redis queue
SERVER_SLEEP = 0.05

ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST", "localhost")
>>>>>>> ciro
