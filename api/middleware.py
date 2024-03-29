import json
import time
import logging
import redis
import settings
from typing import List, Dict

logging.basicConfig(level=20)
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP, port=settings.REDIS_PORT, db=settings.REDIS_DB_ID
)


def model_predict(messages: List[Dict[str, str]], job_id: str) -> str:
    """Pushes a text generation job to redis, and waits for the generative model response

    Args:
        messages (List[Dict[str, str]]): message history
        job_id (str): To be used as redis job ID.

    Returns:
        str: response of the model
    """
    content = None

    job_data = {"id": job_id, "messages": messages}

    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

    while True:
        output = db.get(job_id)

        if output is not None:
            output = json.loads(output.decode("utf-8"))
            content = output["content"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return content
