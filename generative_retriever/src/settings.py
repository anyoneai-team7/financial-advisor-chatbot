import os
from dotenv import load_dotenv, find_dotenv

# load ChatGPT_Key from .env
load_dotenv()
_ = load_dotenv(find_dotenv())

API_KEY = os.getenv("OPENAI_API_KEY")

# REDIS
# Queue name
REDIS_QUEUE = "service_queue"
# Port
REDIS_PORT = 6379
# DB Id
REDIS_DB_ID = 0
# Host IP
REDIS_IP = "localhost"
# Sleep parameters which manages the
# interval between requests to our redis queue
SERVER_SLEEP = 0.05

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
