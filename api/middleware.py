import json
import time
from uuid import uuid4

import redis
import settings

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host= settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
)


def model_predict():

    prediction = None
    score = None

    job_id = str(uuid4())

    job_data = {
        "id": job_id
    }


    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

    while True:

        output = db.get(job_id)


        if output is not None:
            output = json.loads(output.decode("utf-8"))
            prediction = output["prediction"]
            score = output["score"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return prediction, score
