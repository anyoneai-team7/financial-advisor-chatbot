import json
import os
import time

import redis
import settings

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import PromptTemplate
from haystack.nodes import PromptNode
from haystack import Pipeline

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID,
)

### Create your retriver-generative model and assign to variable `model`
# Get the host where Elasticsearch is running, default to localhost
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")
document_store = ElasticsearchDocumentStore(
    host=host, username="", password="", index="document"
)

# Create an instance of BM25Retriver to select top_k better documents into document_store
retriever = BM25Retriever(document_store=document_store)

# Create an instance of PromTemplate, we use the type question-answering
qa_prompt = PromptTemplate(
    name="question-answering",
    prompt_text="""Given the context please answer the question. 
            Your answer should be in your own words and be no longer than 50 words. 
            Context: {join(documents)}; 
            Question:  {query}; 
            Answer:""",
)

# Create an instance of PromptNode using ChatGPT API as generator,
# get API key using settings.py
generator = PromptNode(
    "gpt-3.5-turbo",
    api_key=settings.API_KEY,
    default_prompt_template=qa_prompt,
    model_kwargs={"stream": True},
)

# Pipeline Retriver-Generator
model = Pipeline()
model.add_node(component=retriever, name="retriever", inputs=["Query"])
model.add_node(component=generator, name="generator", inputs=["retriever"])


# Function to receive a query and get the response and return it
def generative_predict(json_user_name, query_num):
    """
    Load a query from the corresponding folder based
    on the jason_query_name (every user have a json file with the cuestion) received, then, run the retriver-generative
    model to get the answer

    Parameters
    ----------
    query_id : str
        query unique identifier.

    Returns
    -------
    answer, context : tuple(str, list)
        Model generate answer as a string and the corresponding context as
        a list of documents.
    """
    # create the path of the user query json
    json_user_path = os.path.join(settings.UPLOAD_FOLDER, json_user_name)

    # read the json user
    with open(json_user_path, "r") as f:
        json_user = json.load(f)

    # get the query into de json user
    user_query = json_user[query_num]["query"]

    # run de model ang get the answer
    output = model.run(
        query=user_query,
        params={
            "retriever": {"top_k": 2},
        },
    )

    # save the answer in the json_user
    json_user[query_num]["answer"] = output["results"]
    with open(json_user_path, "w") as f:
        json.dump(json_user, f, indent=4)

    # return answer and its context
    return output["results"], output["invocation_context"]


# Receive a query and get the response using retriver-generative and return it to the hash table
def get_answer():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the created generative
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    try:
        while True:
            # Inside this loop you should add the code to:
            #   1. Take a new job from Redis
            _, JobDict = db.brpop(settings.REDIS_QUEUE)
            #   2. Run your ML model on the given data
            JobDec = json.loads(JobDict.decode("utf-8"))

            answer, context = generative_predict(
                JobDec["json_name"], JobDec["query_number"]
            )
            #   3. Store generative model answer in a dict with the following shape:
            Out_dict = {"answer": answer, "context": "context"}
            #   4. Store the results on Redis using the original job ID as the key
            db.set(JobDec["id"], json.dumps(Out_dict))
            #   so the API can match the results it gets to the original job
            #   sent
            #   Hint: You should be able to successfully implement the communication
            #   code with Redis making use of functions `brpop()` and `set()`.

            # Sleep for a bit
            time.sleep(settings.SERVER_SLEEP)

    except KeyboardInterrupt:
        print("Function stopped.")


if __name__ == "__main__":
    # Now launch process
    print("Generative service ready")
    get_answer()
