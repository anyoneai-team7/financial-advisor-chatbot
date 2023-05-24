import json
import os
import time

import redis
import settings

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import (
    BM25Retriever,
    SentenceTransformersRanker,
    PromptTemplate,
    PromptNode,
    Shaper,
)
from haystack import Pipeline
from haystack.agents import Agent, Tool

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
retriever = BM25Retriever(document_store=document_store, top_k=10)

# ranked to have a better sorted list of relevant documents using a Cross-Encoder model .
ranker = SentenceTransformersRanker(
    model_name_or_path="cross-encoder/ms-marco-MiniLM-L-12-v2", top_k=3
)

from haystack.nodes import Shaper

# Doing our own pipeline

# shaper is used to join all documents returned by retriver
# shaper = Shaper(func="join_documents", inputs={"documents": "documents"}, outputs=["documents"])

# creating a pipeline
pipeline = Pipeline()

# Add retriver node (BM25retriver)
pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])

# Ranker to get a sorted list of relevant documents
pipeline.add_node(component=ranker, name="Ranker", inputs=["Retriever"])

# Add shaper node to join all documents
# pipeline.add_node(component=shaper, name="Shaper", inputs=["Ranker"])


# Let's create the prompt for the Agent's PromptNode
# Prompt template
zero_shot_react_template = PromptTemplate(
    name="zero-shot-react",
    prompt_text="You are a friendly chatbot working as a financial assistant and you are having a conversation with a user."
    "At the end of the conversation, the user tells you something which is usually a new question. If you know the answer, respond immediately. "
    "If you don't know the answer, to achieve your goal of answering complex questions correctly, you have access to the following tool:\n\n"
    "Documents: Receives a question to try to find the answer information in a Document store. \n\n"
    "To answer questions, you'll need to go through multiple steps involving step-by-step. "
    "thinking and selecting when to use the Search_Documents tool; the tool will respond with Observations."
    "If after searching you feel that the user should enter any additional data, return a response requesting it."
    "When you are ready for a final answer, respond with the `Final Answer:`\n\n"
    "Use the following format:\n\n"
    "Question: the question to be answered\n"
    "Thought: Reason if you have the final answer. If yes, answer the question. If not, rephrase the question to search with the Documents tool.\n"
    "Tool: Documents \n"
    "Tool Input: a question to find the missing information needed to answer \n"
    "Observation: the tool will respond with the result in no more 50 words \n"
    "...\n"
    "Final Answer: the final answer to the question, in no more than 50 words\n\n"
    "Thought, Tool, Tool Input, and Observation steps can be repeated multiple times, but sometimes we can find an answer in the first pass\n"
    "---\n\n"
    "Question: {query}\n"
    "Thought: Let's think step-by-step, I first need to ",
)  # output_parser=AnswerParser()
# PromptNode using
prompt_node = PromptNode(
    "gpt-3.5-turbo",
    api_key=settings.API_KEY,
    max_length=512,
    model_kwargs={
        "stream": True,
        "temperature": 0,
    },  # max_length=512, stop_words=["Observation:"],
)

# Let's configure Search in docuement store as the Agent's tool
# Each tool needs to have a description that helps the Agent decide when to use it
search_in_ds = Tool(
    name="Documents",
    pipeline_or_node=pipeline,
    description="Receives a question to try to find the answer information in a Document store",
    output_variable="documents",
)

# Time to initialize the Agent specifying the PromptNode to use and the Tools
agent = Agent(
    prompt_node=prompt_node,
    prompt_template=zero_shot_react_template,
    final_answer_pattern=r"Final Answer\s*:\s*(.*)",
)
# Add tool to the agent
agent.add_tool(tool=search_in_ds)


# Function to receive a query and get the response and return it
def generative_predict(chat_history):
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

    # get the query into de json user
    user_query = " \n".join(
        [f"{item['role']}: {item['conten']}" for item in chat_history]
    )

    # run de model agent and get the answer
    result = agent.run(query=user_query)
    # return answer
    return result["answers"][0].answer


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

            answer = generative_predict(JobDec["messages"])
            #   3. Store generative model answer in a dict with the following shape:
            Out_dict = {"answer": answer}
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
