import json
from typing import List
import time
import redis
from src.lang_agent import make_agent
from src import settings
from dotenv import load_dotenv

from langchain.schema import BaseMessage, HumanMessage, AIMessage, messages_from_dict

# create agent
load_dotenv()
agent = make_agent()

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID,
)


# Function to receive chat history and get the last query, response and return it
def agent_predict(chat_history: List[BaseMessage]) -> str:
    """
    Recive the the last query and chat_history

    Parameters
    ----------
    chat_history : List[BaseMessage]
        List of messages.

    Returns
    -------
    answer, chat_history : tuple(str, list)
        Model return answer as a string and update the chat history.
    """

    # get the query into the chat history
    query = chat_history[-1].content

    # Run the agent with the query and chat history
    output = agent(
        {
            "input": query,
            "chat_history": chat_history,
        }
    )["output"]

    # updating chat history
    # chat_history.append(HumanMessage(content=query))
    # chat_history.append(AIMessage(content=output))

    return output


# Receive a query and get the response using retriver-generative and return it to the hash table
def get_answer():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the created agent
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    """
    while True:
        #   1. Take a new job from Redis
        _, JobDict = db.brpop(settings.REDIS_QUEUE)
        #   2. Run your agent model on the given query
        JobDec = json.loads(JobDict.decode("utf-8"))
        chat_history = messages_from_dict(JobDec["chat_history"])
        answer = agent_predict(chat_history)
        #   3. Store generative model answer in a dict with the following shape:
        Out_dict = {"answer": answer}
        #   4. Store the results on Redis using the original job ID as the key
        db.set(JobDec["id"], json.dumps(Out_dict))
        #   so the API can match the results it gets to the original job sent
        # Sleep for a bit
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Agent service ready")
    get_answer()
