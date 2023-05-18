from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

# load ChatGPT_Key from .env
load_dotenv()
_ = load_dotenv(find_dotenv())

API_KEY = os.getenv("GPT_KEY")

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

# We will store images uploaded by the user on this folder
UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
