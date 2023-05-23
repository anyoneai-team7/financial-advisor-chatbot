import json
import time

import redis
import settings

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host= settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
)


def model_predict(api_input):

    user = None
    content = None

    job_id = api_input["user"]

    job_data = {
        "id": job_id,
        "messages": api_input["messages"]
    }


    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

    while True:

        output = db.get(job_id)


        if output is not None:
            output = json.loads(output.decode("utf-8"))
            user = output["user"]
            content = output["content"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return user, content
